"""Import existing IF.data exports into the immutable raw archive.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

import json
from pathlib import Path

from loguru import logger

from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.storage.collection import (
    legacy_report_inputs,
    publish_local_report,
    report_checksum,
    report_inputs,
    validate_report_csv,
)


def _has_version(directory: Path, checksum: str) -> bool:
    """Find a published bundle with the same verified bytes.

    Args:
        directory: Raw directory for one report month.
        checksum: Hash of the validated flat CSV.
    Returns:
        Whether an immutable bundle already contains that content.
    Raises:
        KeyError: A manifest is missing its checksum.
        OSError: A candidate bundle cannot be read.
        TypeError: A candidate manifest is not a mapping.
        ValueError: A candidate manifest has invalid JSON.
    """
    for manifest in directory.glob('*/metadata.json'):
        version = manifest.with_name('report.csv')
        metadata = json.loads(manifest.read_text(encoding='utf-8'))
        if (
            metadata['sha256'] == checksum
            and version.is_file()
            and report_checksum(version) == checksum
        ):
            return True
    return False


def version_local_reports(
    raw_root: Path,
    scratch: Path,
    *,
    institution: str | None = None,
    report: str | None = None,
    period: str | None = None,
) -> None:
    """Archive flat CSVs and retain the selection already used downstream.

    Args:
        raw_root: Existing raw IF.data collection.
        scratch: Workspace for atomic staging.
        institution: Optional institutional scope directory name.
        report: Optional report directory name.
        period: Optional reference month in YYYY-MM.
    Returns:
        None.
    Raises:
        IfDataScraperException: A month lacks a valid original or publication
            could not be completed.
        FileNotFoundError: The raw directory does not exist.
    """
    if not raw_root.is_dir():
        raise FileNotFoundError(f'Raw IF.data directory not found: {raw_root}')

    published = archived = duplicates = rejected = 0
    failures = []
    for directory in sorted(raw_root.glob('*/*')):
        if not directory.is_dir():
            continue
        if institution and directory.parent.name != institution.lower():
            continue
        if report and directory.name != report.lower():
            continue
        legacy = legacy_report_inputs(directory)
        active = report_inputs(directory)
        for month, source in sorted(legacy.items()):
            if period and month != period:
                continue
            date = f'{month[5:]}/{month[:4]}'
            selected = active.get(month, source)
            try:
                checksum = report_checksum(source)
                validate_report_csv(source, date)
            except (IfDataScraperException, OSError) as error:
                rejected += 1
                logger.warning(f'Rejected legacy source {source}: {error}')
                if selected == source:
                    failures.append(f'{source}: {error}')
                else:
                    try:
                        validate_report_csv(selected, date)
                    except (IfDataScraperException, OSError) as active_error:
                        failures.append(f'{source}: {active_error}')
                continue

            destination = source.with_suffix('')
            try:
                if _has_version(destination, checksum):
                    duplicates += 1
                    continue
                archive_only = selected != source
                publish_local_report(
                    source, raw_root, scratch, checksum,
                    archive_only=archive_only,
                )
            except (
                IfDataScraperException, KeyError, OSError, TypeError,
                ValueError,
            ) as error:
                logger.warning(f'Could not version {source}: {error}')
                failures.append(f'{source}: {error}')
            else:
                archived += int(archive_only)
                published += int(not archive_only)

    logger.info(
        f'Local CSV versioning: {published} active copies, {archived} '
        f'archived copies, {duplicates} already versioned, '
        f'{rejected} rejected originals, {len(failures)} unresolved.'
    )
    if failures:
        raise IfDataScraperException('\n'.join(failures))
