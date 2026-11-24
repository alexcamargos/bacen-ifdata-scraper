"""Update changed IF.data periods and publish a tested warehouse release.

Args:
    None.

Returns:
    None.

Raises:
    None.
"""

import json
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, date, datetime
from enum import StrEnum
from hashlib import file_digest, sha256
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
from uuid import uuid4

import duckdb
from loguru import logger

from bacen_ifdata.data_cleaner.processing import normalize_csv
from bacen_ifdata.data_loader.storage import DatabaseService
from bacen_ifdata.data_transformer.interfaces.controller import (
    TransformerControllerInterface,
)
from bacen_ifdata.data_transformer.schemas.mapper import (
    SCHEMA_BY_INSTITUTION_AND_REPORT,
)
from bacen_ifdata.scraper.institutions import InstitutionType
from bacen_ifdata.scraper.storage.collection import (
    report_checksum,
    report_inputs,
    validate_report_csv,
)
from bacen_ifdata.scraper.storage.processing import move_artifact
from bacen_ifdata.utilities.configurations import Config
from bacen_ifdata.utilities.releases import CURRENT_RELEASE, current_release

SOURCE = 'bcb.ifdata.portal'
LEDGER = 'ifdata_control.applied_inputs'
BuildGold = Callable[[Path, Path, Path], None]
InputKey = tuple[str, str, str, date]


@dataclass(frozen=True)
class RawInput:
    """The validated inventory entry for one report and month.

    Args:
        institution: Institutional scope.
        report: Report identifier.
        period: First day of the reference month.
        path: Path to the original export.
        checksum: SHA-256 of the original bytes.
        source_url: Provenance URL.
        collected_at: Timestamp from collection metadata, when recorded.

    Returns:
        None.

    Raises:
        None.
    """

    institution: InstitutionType
    report: StrEnum
    period: date
    path: Path
    checksum: str
    source_url: str
    collected_at: datetime | None

    @property
    def key(self) -> InputKey:
        """Return the input identity used by the Silver ledger.

        Args:
            None.

        Returns:
            Source, scope, report, and date.

        Raises:
            None.
        """
        return (
            SOURCE, self.institution.name.lower(),
            self.report.name.lower(), self.period,
        )


@contextmanager
def _update_lock(root: Path, scratch: Path) -> Iterator[None]:
    """Hold a local DuckDB write lock for one dataset.

    Args:
        root: Root of the data layers.
        scratch: Directory for the lock database.

    Returns:
        A context that releases the lock on exit.

    Raises:
        duckdb.Error: Another writer owns the update lock or it is unreadable.
    """
    identifier = sha256(str(root).encode('utf-8')).hexdigest()[:16]
    path = scratch / f'ifdata_update_{identifier}.duckdb'
    with duckdb.connect(str(path)) as connection:
        connection.execute(
            'CREATE TABLE IF NOT EXISTS writer (id INTEGER PRIMARY KEY)'
        )
        connection.execute('INSERT OR IGNORE INTO writer VALUES (1)')
        connection.begin()
        connection.execute('UPDATE writer SET id = 1 WHERE id = 1')
        try:
            yield
        finally:
            connection.rollback()


def _inventory() -> dict[InputKey, RawInput]:
    """Find the newest original for each key and verify recorded hashes.

    Args:
        None.

    Returns:
        Export records indexed by source, scope, report and month.

    Raises:
        ValueError: A version's metadata does not match its original.
        OSError: A raw input or its metadata cannot be read.
    """
    inputs = {}
    for institution, reports in SCHEMA_BY_INSTITUTION_AND_REPORT.items():
        for report in reports:
            directory = (
                Config.DOWNLOAD_DIRECTORY
                / institution.name.lower()
                / report.name.lower()
            )
            for month, path in sorted(report_inputs(directory).items()):
                checksum = report_checksum(path)
                source_url = Config.URL
                collected_at = None
                if path.name == 'report.csv':
                    metadata = json.loads(
                        path.with_name('metadata.json').read_text(
                            encoding='utf-8',
                        )
                    )
                    if metadata['sha256'] != checksum:
                        raise ValueError(f'Raw checksum mismatch: {path}')
                    source_url = metadata['source_url']
                    collected_at = datetime.fromisoformat(
                        metadata['collected_at'],
                    )
                entry = RawInput(
                    institution, report, date.fromisoformat(f'{month}-01'),
                    path, checksum, source_url, collected_at,
                )
                inputs[entry.key] = entry
    return inputs


def _fingerprint(root: Path, paths: list[Path]) -> str:
    """Hash file identities and contents in a deterministic order.

    Args:
        root: Base used for stable relative paths.
        paths: Files to include in the fingerprint.

    Returns:
        A SHA-256 fingerprint.

    Raises:
        OSError: A rule file could not be read.
    """
    digest = sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode('utf-8'))
        digest.update(b'\0')
        with path.open('rb') as handle:
            digest.update(file_digest(handle, 'sha256').digest())
    return digest.hexdigest()


def _revisions() -> tuple[str, str]:
    """Identify changes to Silver rules and to the dbt project separately.

    Args:
        None.

    Returns:
        Fingerprints for the transformation rules and the analytical models.

    Raises:
        OSError: A rule file could not be read.
    """
    package = Path(__file__).parent
    transformation = [
        Path(__file__),
        package / 'data_cleaner/processing.py',
        package / 'data_loader/storage.py',
        package / 'utilities/csv_loader.py',
        package / 'utilities/geographic_regions.py',
        package / 'utilities/string_utils.py',
        *package.joinpath('data_transformer').rglob('*.py'),
    ]
    project = Config.DATA_ANALYTICS_DIRECTORY
    project_files = (
        'dbt_project.yml', 'profiles.yml', 'packages.yml',
        'package-lock.yml', 'dependencies.yml', 'selectors.yml',
    )
    models = [
        project / filename for filename in project_files
        if (project / filename).is_file()
    ]
    for name in ('models', 'macros', 'seeds', 'snapshots', 'tests'):
        models.extend(
            path for path in (project / name).rglob('*')
            if path.suffix in {'.sql', '.yml', '.yaml', '.csv', '.py'}
            and path.is_file()
        )
    return _fingerprint(package, transformation), _fingerprint(project, models)


def _applied_inputs(silver: Path) -> dict[InputKey, tuple[str, str]]:
    """Read the load ledger without writing to the published database.

    Args:
        silver: Published Silver database.

    Returns:
        The raw hash and transformation revision for each applied input.

    Raises:
        duckdb.Error: The published ledger is missing or unreadable.
    """
    with duckdb.connect(str(silver), read_only=True) as connection:
        rows = connection.execute(
            f'SELECT source, institution, report, data_base, sha256, revision '
            f'FROM {LEDGER}'
        ).fetchall()
    return {tuple(row[:4]): tuple(row[4:]) for row in rows}


def _load_changes(
    silver: Path,
    workspace: Path,
    changed: list[RawInput],
    revision: str,
    transformer: TransformerControllerInterface,
) -> None:
    """Transform selected inputs and replace their complete Silver periods.

    Args:
        silver: Candidate Silver database.
        workspace: Temporary directory for cleaned and typed CSV files.
        changed: New or explicitly revised inputs.
        revision: Fingerprint of the transformation rules.
        transformer: The existing report transformation controller.

    Returns:
        None.

    Raises:
        ValueError: A transformed period has invalid or repeated keys.
        OSError: The export could not be normalized or written.
        duckdb.Error: A transaction failed.
    """
    database = DatabaseService(silver)
    tables = set()
    try:
        connection = database.connection
        connection.execute('CREATE SCHEMA IF NOT EXISTS ifdata_control')
        connection.execute(f'''
            CREATE TABLE IF NOT EXISTS {LEDGER} (
                source VARCHAR, institution VARCHAR, report VARCHAR,
                data_base DATE, sha256 VARCHAR NOT NULL,
                revision VARCHAR NOT NULL, source_url VARCHAR NOT NULL,
                collected_at TIMESTAMPTZ, raw_path VARCHAR NOT NULL,
                row_count BIGINT NOT NULL,
                PRIMARY KEY (source, institution, report, data_base)
            )
        ''')
        cleaned = workspace / 'cleaned.csv'
        typed = workspace / 'typed.csv'
        for entry in changed:
            _, institution, report, period = entry.key
            table = f'{institution}_{report}'
            schema = SCHEMA_BY_INSTITUTION_AND_REPORT[entry.institution][
                entry.report
            ]
            validate_report_csv(entry.path, period.strftime('%m/%Y'))
            if not normalize_csv(
                entry.institution, entry.report, entry.path.name,
                source=entry.path, destination=cleaned,
            ):
                raise OSError(f'Could not normalize {entry.path}')
            data = transformer.transform(cleaned, schema, entry.institution)
            data.to_csv(typed, index=False)
            if table not in tables:
                database.create_table(table, schema)
                tables.add(table)
            connection.begin()
            try:
                connection.execute(
                    f'CREATE TEMP TABLE ifdata_input AS '
                    f'SELECT * FROM {table} LIMIT 0'
                )
                database.insert_data('ifdata_input', typed, schema)
                rows, codes, dates = connection.execute(
                    'SELECT count(*), count(DISTINCT codigo), '
                    'count(*) FILTER (WHERE data_base = ?) FROM ifdata_input',
                    [period],
                ).fetchone()
                if not rows or rows != codes or rows != dates:
                    raise ValueError(
                        f'{entry.path}: invalid institution or date keys.'
                    )
                connection.execute(
                    f'DELETE FROM {table} WHERE data_base = ?', [period],
                )
                connection.execute(
                    f'INSERT INTO {table} SELECT * FROM ifdata_input',
                )
                connection.execute(
                    f'INSERT OR REPLACE INTO {LEDGER} '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    [
                        *entry.key, entry.checksum, revision,
                        entry.source_url, entry.collected_at,
                        str(entry.path.relative_to(Config.DATA_DIRECTORY)),
                        rows,
                    ],
                )
                connection.execute('DROP TABLE ifdata_input')
                connection.commit()
            except (OSError, ValueError, duckdb.Error):
                connection.rollback()
                raise
    finally:
        database.close()


def update_warehouse(
    transformer: TransformerControllerInterface, build_gold: BuildGold,
) -> int:
    """Publish a new pair only when an input or a model has changed.

    Args:
        transformer: Report transformation controller.
        build_gold: Runner that must raise if the dbt build fails.

    Returns:
        Number of inputs transformed and loaded into the release.

    Raises:
        ValueError: Inputs are missing or a validation failed.
        OSError: A candidate or pointer could not be published.
        duckdb.Error: The ledger, update lock, or data load failed.
        subprocess.CalledProcessError: The dbt build failed.
    """
    root = Config.DATA_DIRECTORY
    scratch = Config.SCRATCH_DIRECTORY
    scratch.mkdir(parents=True, exist_ok=True)
    with _update_lock(root, scratch):
        current = current_release(root)
        inputs = _inventory()
        if not inputs:
            raise ValueError('No IF.data originals were found.')
        applied = _applied_inputs(current.silver) if current else {}
        missing = applied.keys() - inputs.keys()
        if missing:
            raise ValueError(
                f'Previously applied originals are missing: {sorted(missing)}'
            )
        revision, model_revision = _revisions()
        refresh_all = any(old != revision for _, old in applied.values())
        changed = [
            entry for key, entry in inputs.items()
            if refresh_all or applied.get(key) != (entry.checksum, revision)
        ]
        models_unchanged = current and current.model_revision == model_revision
        if not changed and models_unchanged:
            logger.info('Inputs and models unchanged. Kept current release.')
            return 0
        logger.info(f'Loading {len(changed)} of {len(inputs)} inputs.')
        version = (
            datetime.now(UTC).strftime('%Y%m%dT%H%M%S%fZ')
            + '-' + uuid4().hex[:8]
        )
        silver = Path('interim/releases') / version / 'silver_warehouse.duckdb'
        gold = Path('processed/releases') / version / 'gold_warehouse.duckdb'
        with TemporaryDirectory(dir=scratch) as temporary:
            workspace = Path(temporary)
            draft_silver = workspace / silver.name
            draft_gold = workspace / gold.name
            if current and not refresh_all:
                copyfile(current.silver, draft_silver)
            if changed:
                _load_changes(
                    draft_silver, workspace, changed, revision, transformer,
                )
            build_gold(draft_silver, draft_gold, workspace)
            for draft, destination in (
                (draft_silver, root / silver), (draft_gold, root / gold),
            ):
                destination.parent.mkdir(parents=True, exist_ok=True)
                move_artifact(draft, destination)
            pointer = workspace / CURRENT_RELEASE.name
            pointer.write_text(
                json.dumps({
                    'silver': silver.as_posix(), 'gold': gold.as_posix(),
                    'model_revision': model_revision,
                }, indent=2) + '\n',
                encoding='utf-8',
            )
            move_artifact(pointer, root / CURRENT_RELEASE, replace=True)
        logger.info(f'Published warehouse release {version}.')
        return len(changed)
