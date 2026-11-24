"""Plan and resume IF.data CSV collection.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

from collections.abc import Callable
from enum import StrEnum
from itertools import chain
from pathlib import Path
from tempfile import TemporaryDirectory

from loguru import logger

from bacen_ifdata.interfaces import SessionProtocol
from bacen_ifdata.main.scraper import publish_export
from bacen_ifdata.scraper.catalog import (
    HistoricalReport,
    historical_reports,
)
from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.institutions import InstitutionType
from bacen_ifdata.scraper.storage.collection import PERIOD, report_inputs
from bacen_ifdata.scraper.storage.validation_cache import ValidationCache
from bacen_ifdata.utilities.configurations import Config

Target = tuple[InstitutionType, StrEnum]
InputKey = tuple[InstitutionType, StrEnum, str]


def _valid(
    cache: ValidationCache, path: Path, period: str, *, force: bool,
) -> bool:
    """Check a local export and report invalid originals for recollection.

    Args:
        cache: File validation cache for the raw directory.
        path: Active local version.
        period: Reference month in YYYY-MM format.
        force: Read the file even if previously validated.
    Returns:
        Whether the original is structurally valid for the period.
    Raises:
        None.
    """
    try:
        cache.validate(path, period, force=force)
    except (IfDataScraperException, OSError) as error:
        logger.warning(f'Recollection required: {error}')
        return False
    return True


def _collect(
    session: SessionProtocol,
    selection: HistoricalReport,
    existing: Path | None,
    receipt: Path,
) -> tuple[Path, bool]:
    """Fetch, validate and publish one export with one retry on failure.

    Args:
        session: Browser session for the historical source.
        selection: Exact source entry for the report.
        existing: Active original before the collection.
        receipt: Job-owned scratch file for the exported bytes.
    Returns:
        Active version and whether a new one was published.
    Raises:
        IfDataScraperException: Both attempts to export or validate failed.
        OSError: The CSV could not be persisted.
    """
    destination = (
        Config.DOWNLOAD_DIRECTORY
        / selection.institution.name.lower()
        / selection.report.name.lower()
        / selection.period
    )
    for attempt in (1, 2):
        try:
            contents = session.export_historical_report(
                selection, fresh=attempt == 2,
            )
            receipt.write_bytes(contents)
            return publish_export(
                receipt, destination, existing,
                source_selection={
                    'institution_id': selection.institution_id,
                    'report_id': selection.report_id,
                },
                source_url=selection.source_url,
            )
        except IfDataScraperException as error:
            if attempt == 2:
                raise
            logger.warning(f'Retrying {destination}: {error}')


def run_historical_collection(
    targets: list[Target],
    session_factory: Callable[[], SessionProtocol | None],
    *,
    period: str | None,
    refresh: bool,
    repair: bool,
    include_current: bool = False,
) -> None:
    """Match the selected catalogs to active originals and collect gaps.

    Args:
        targets: Institutional scopes and report types selected by the CLI.
        session_factory: Opens a browser only when an export is needed.
        period: Optional reference month to collect in YYYY-MM format.
        refresh: Export the selected month again to look for revisions.
        repair: Revalidate and recollect only invalid local originals.
        include_current: Discover reports from 2025 onward as well.
    Returns:
        None.
    Raises:
        ValueError: The requested period or selection is invalid.
        IfDataScraperException: The catalog or one or more exports failed.
    """
    historical_end = Config.HISTORICAL_END
    if period and not PERIOD.fullmatch(period):
        raise ValueError(f'Invalid IF.data reference month: {period}.')
    if period and period > historical_end and not include_current:
        raise ValueError(
            f'Historical IF.data collection ends at {historical_end}.'
        )

    root = Config.DOWNLOAD_DIRECTORY
    scratch = Config.SCRATCH_DIRECTORY
    cache = ValidationCache(root, scratch)
    inventory = {
        (institution, report, month): path
        for institution, report in targets
        for month, path in report_inputs(
            root / institution.name.lower() / report.name.lower(),
        ).items()
        if (include_current or month <= historical_end)
        and (period is None or period == month)
    }
    target_set = set(targets)

    try:
        repairs = set()
        if repair:
            repairs = {
                key for key, path in inventory.items()
                if not _valid(cache, path, key[2], force=True)
            }
            if not repairs:
                logger.info('No invalid originals found in the selection.')
                return

        periods = {key[2] for key in repairs} if repair else {period}
        historical = (
            historical_reports(Config.TIMEOUT)
            if any(
                month is None or month <= historical_end for month in periods
            )
            else []
        )
        current = (
            historical_reports(Config.TIMEOUT, current=True)
            if include_current
            and any(
                month is None or month > historical_end for month in periods
            )
            else []
        )
        advertised = {
            (item.institution, item.report, item.period): item
            for item in chain(historical, current)
            if (item.institution, item.report) in target_set
            and (period is None or item.period == period)
            and (not repair or (item.institution, item.report, item.period)
                 in repairs)
        }
        if not repair and not advertised:
            date_filter = period or 'all periods'
            raise ValueError(f'No IF.data report matches {date_filter}.')

        unavailable = repairs - advertised.keys()
        failed = [
            f'{institution.name}/{report.name}/{month}: unavailable in catalog'
            for institution, report, month in sorted(unavailable)
        ]
        pending = {
            key: item for key, item in advertised.items()
            if refresh or repair or key not in inventory
            or not _valid(cache, inventory[key], item.period, force=False)
        }
        logger.info(
            f'IF.data catalog: {len(advertised)} selected, '
            f'{len(advertised) - len(pending)} available locally, '
            f'{len(pending)} to export.'
        )

        published_count = 0
        unchanged_count = 0
        if pending:
            session = session_factory()
            if session is None:
                raise ValueError('Session is required for scraping.')
            scratch.mkdir(parents=True, exist_ok=True)
            with TemporaryDirectory(dir=scratch) as stage:
                receipt = Path(stage) / 'dados.csv'
                for key, selection in pending.items():
                    try:
                        path, published = _collect(
                            session, selection, inventory.get(key), receipt,
                        )
                    except (IfDataScraperException, OSError) as error:
                        outcome = (
                            f'{selection.institution.name}/'
                            f'{selection.report.name}/{selection.period}: '
                            f'{error}'
                        )
                        logger.warning(outcome)
                        failed.append(outcome)
                    else:
                        cache.remember(path, selection.period)
                        published_count += int(published)
                        unchanged_count += int(not published)

        logger.info(
            f'IF.data collection: {published_count} versions published, '
            f'{unchanged_count} identical exports, {len(failed)} failures.'
        )
        if failed:
            raise IfDataScraperException(
                f'{len(failed)} pending exports:\n' + '\n'.join(failed)
            )
    finally:
        cache.save()
