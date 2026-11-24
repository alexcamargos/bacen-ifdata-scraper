"""Validate and version the original IF.data CSV exports.

Args:
    None.

Returns:
    None.

Raises:
    None.
"""

import csv
import json
import re
from datetime import UTC, datetime
from hashlib import file_digest
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
from uuid import uuid4

from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.storage.processing import (
    move_artifact,
    retry_file_lock,
)

PERIOD = re.compile(r'[0-9]{4}-(?:0[1-9]|1[0-2])')
REPORT_DATE = re.compile(r'(?:0[1-9]|1[0-2])/[0-9]{4}')
INSTITUTION_CODE = re.compile(r'[0-9]+(?:\.[0-9]+)*')
LOCAL_ARCHIVE_PREFIX = '0000-archive-'
# A local baseline sorts before any timestamped publication.
LOCAL_VERSION = '0000-local'


def report_checksum(path: Path) -> str:
    """Compute the SHA-256 of an original export.

    Args:
        path: File to hash.

    Returns:
        The SHA-256 hexadecimal digest.

    Raises:
        OSError: The file could not be read.
    """
    file = retry_file_lock(lambda: path.open('rb'), path)
    with file as handle:
        return file_digest(handle, 'sha256').hexdigest()


def validate_report_csv(path: Path, expected_date: str) -> None:
    """Require a dated IF.data export for the requested reference month.

    Args:
        path: Original portal CSV, including any grouped headers or totals.
        expected_date: Reference month in MM/YYYY format.

    Returns:
        None.

    Raises:
        IfDataScraperException: The CSV is unreadable or has invalid data.
    """
    dates: set[str] = set()
    try:
        file = retry_file_lock(
            lambda: path.open(encoding='utf-8-sig', newline=''), path,
        )
        with file as source:
            reader = csv.reader(source, delimiter=';')
            header = [cell.strip().casefold() for cell in next(reader, [])]
            if 'data' not in header or 'código' not in header:
                raise IfDataScraperException(
                    f'{path}: missing Data or Código in the IF.data header.'
                )
            date_index = header.index('data')
            code_index = header.index('código')
            columns = len(header) - int(not header[-1])
            for row in reader:
                if len(row) <= code_index:
                    continue
                if not INSTITUTION_CODE.fullmatch(row[code_index].strip()):
                    continue
                if len(row) == columns + 1 and not row[-1]:
                    row.pop()
                if len(row) != columns:
                    raise IfDataScraperException(
                        f'{path}: wrong column count on line {reader.line_num}'
                    )
                date = row[date_index].strip()
                if not REPORT_DATE.fullmatch(date):
                    raise IfDataScraperException(
                        f'{path}: invalid data-base on line {reader.line_num}.'
                    )
                dates.add(date)
    except (OSError, UnicodeError, csv.Error) as error:
        raise IfDataScraperException(
            f'{path}: could not read the IF.data CSV headers or rows ({error})'
        ) from error

    if dates != {expected_date}:
        found = ', '.join(sorted(dates)) or 'no dated rows'
        raise IfDataScraperException(
            f'{path}: expected data-base {expected_date}, found {found}.'
        )


def legacy_report_inputs(directory: Path) -> dict[str, Path]:
    """Find flat CSVs named after their reference month.

    Args:
        directory: Raw directory for a report and institutional scope.
    Returns:
        Legacy CSVs indexed by YYYY-MM.
    Raises:
        OSError: The directory cannot be read.
    """
    return {
        path.stem: path
        for path in directory.glob('*.csv')
        if PERIOD.fullmatch(path.stem) and path.is_file()
    }


def report_inputs(directory: Path) -> dict[str, Path]:
    """Resolve the most recent published version of each reference month.

    Args:
        directory: Raw directory for a report and institutional scope.

    Returns:
        Source CSVs indexed by reference month in YYYY-MM format.

    Raises:
        OSError: If the directory cannot be read.
    """
    inputs = legacy_report_inputs(directory)
    for metadata in sorted(directory.glob('*/*/metadata.json')):
        if metadata.parent.name.startswith(LOCAL_ARCHIVE_PREFIX):
            continue
        period = metadata.parent.parent.name
        version = metadata.with_name('report.csv')
        if PERIOD.fullmatch(period) and version.is_file():
            inputs[period] = version
    return inputs


def publish_report(
    downloaded: Path,
    destination: Path,
    source_url: str,
    scratch: Path,
    *,
    source_selection: dict[str, int] | None = None,
) -> Path:
    """Publish an immutable original and its metadata together.

    Args:
        downloaded: Validated CSV exported by the browser.
        destination: Raw directory for the scope, report and YYYY-MM.
        source_url: URL of the source portal.
        scratch: Temporary workspace on the same volume as the destination.
        source_selection: IDs from the source catalog, when available.

    Returns:
        Path of the published original CSV.

    Raises:
        OSError: If copying or publishing the files fails.
    """
    collected_at = datetime.now(UTC)
    stamp = collected_at.strftime('%Y%m%dT%H%M%S%fZ')
    version = destination / f'{stamp}-{uuid4().hex}'
    provenance: dict[str, str | dict[str, int]] = {
        'source_url': source_url,
        'collected_at': collected_at.isoformat(),
    }
    if source_selection is not None:
        provenance['source_selection'] = source_selection
    return _publish_bundle(downloaded, version, scratch, provenance)


def publish_local_report(
    source: Path,
    raw_root: Path,
    scratch: Path,
    checksum: str,
    *,
    archive_only: bool,
) -> Path:
    """Publish a byte-identical local original with its actual provenance.

    Args:
        source: Validated flat CSV.
        raw_root: Base for the relative source path.
        scratch: Temporary workspace on the destination volume.
        checksum: SHA-256 of the validated source.
        archive_only: Retain the existing active version.
    Returns:
        Published CSV path.
    Raises:
        IfDataScraperException: The copied bytes differ from the source hash.
        OSError: The bundle cannot be published.
    """
    name = (
        f'{LOCAL_ARCHIVE_PREFIX}{checksum}' if archive_only else LOCAL_VERSION
    )
    version = source.with_suffix('') / name
    return _publish_bundle(
        source, version, scratch,
        {
            'source_type': 'local_csv',
            'source_path': source.relative_to(raw_root).as_posix(),
            'imported_at': datetime.now(UTC).isoformat(),
        },
        expected_checksum=checksum,
    )


def _publish_bundle(
    source: Path,
    version: Path,
    scratch: Path,
    provenance: dict[str, str | dict[str, int]],
    *,
    expected_checksum: str | None = None,
) -> Path:
    """Stage the original and manifest and publish them together.

    Args:
        source: Original bytes to copy.
        version: Final bundle directory.
        scratch: Temporary workspace on the destination volume.
        provenance: Metadata specific to the source.
        expected_checksum: Optional hash required before publication.
    Returns:
        Published CSV path.
    Raises:
        IfDataScraperException: The copy does not match the expected hash.
        OSError: The bundle cannot be copied or published.
    """
    destination = version.parent
    scratch.mkdir(parents=True, exist_ok=True)
    destination.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory(dir=scratch) as temporary:
        bundle = Path(temporary) / 'report'
        bundle.mkdir()
        csv_path = bundle / 'report.csv'
        retry_file_lock(lambda: copyfile(source, csv_path), source)
        checksum = report_checksum(csv_path)
        if expected_checksum is not None and checksum != expected_checksum:
            raise IfDataScraperException(
                f'Original changed during copy: {source}'
            )
        metadata = {
            **provenance,
            'institution': destination.parent.parent.name,
            'report': destination.parent.name,
            'data_base': destination.name,
            'sha256': checksum,
        }
        (bundle / 'metadata.json').write_text(
            json.dumps(metadata, indent=2) + '\n', encoding='utf-8',
        )
        move_artifact(bundle, version)
    return version / 'report.csv'
