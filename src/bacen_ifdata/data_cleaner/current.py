"""Normalize native CSV layouts from the current IF.data portal.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

import csv
from pathlib import Path
from tempfile import TemporaryDirectory

from bacen_ifdata.scraper.storage.collection import (
    INSTITUTION_CODE,
    validate_report_csv,
)
from bacen_ifdata.scraper.storage.consolidation import read_report_layout
from bacen_ifdata.scraper.storage.processing import move_artifact


def clean_current_report(
    source: Path,
    destination: Path,
    period: str,
    raw_root: Path,
    scratch: Path,
) -> None:
    """Write institution rows with all labels and their original position.

    Args:
        source: Original portal export.
        destination: Normalized CSV in staging.
        period: Reference month in YYYY-MM.
        raw_root: Root for the relative original path recorded on each row.
        scratch: Location for the temporary CSV before publication.
    Returns:
        None.
    Raises:
        IfDataScraperException: The source failed portal CSV validation.
        OSError: A CSV could not be read or written.
        ValueError: The source is outside the raw data directory.
    """
    origin = source.relative_to(raw_root).as_posix()
    validate_report_csv(source, f'{period[5:]}/{period[:4]}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=scratch) as temporary:
        stage = Path(temporary) / destination.name
        with (
            source.open(encoding='utf-8-sig', newline='') as stream,
            stage.open('w', encoding='utf-8', newline='') as output,
        ):
            labels, code_index, rows = read_report_layout(stream)
            writer = csv.writer(output, delimiter=';')
            writer.writerow(['arquivo_origem', *labels])
            for row in rows:
                if len(row) > code_index and INSTITUTION_CODE.fullmatch(
                    row[code_index].strip()
                ):
                    writer.writerow([origin, *row[:len(labels)]])
        move_artifact(stage, destination, replace=True)
