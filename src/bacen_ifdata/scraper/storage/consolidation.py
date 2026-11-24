"""Consolidate published IF.data CSVs without converting financial values.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

import csv
from collections import Counter
from collections.abc import Iterator
from itertools import chain
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TextIO

from loguru import logger

from bacen_ifdata.scraper.storage.collection import (
    INSTITUTION_CODE,
    validate_report_csv,
)
from bacen_ifdata.scraper.storage.processing import move_artifact


def _read_layout(
    source: TextIO,
) -> tuple[list[str], int, Iterator[list[str]]]:
    """Resolve grouped headers and return the remaining native data rows.

    Args:
        source: Open, validated CSV with its BOM removed.
    Returns:
        Column labels, institution-code index and iterator over data rows.
    Raises:
        ValueError: The header lacks a required field.
        csv.Error: The CSV could not be parsed.
    """
    reader = csv.reader(source, delimiter=';')
    header = next(reader, [])
    if header and not header[-1]:
        header.pop()
    names = [cell.strip().casefold() for cell in header]
    code_index = names.index('código')
    date_index = names.index('data')
    groups = [header]
    first_row = []
    for row in reader:
        if len(row) > code_index and INSTITUTION_CODE.fullmatch(
            row[code_index].strip()
        ):
            first_row = row
            break
        if (
            len(row) in {len(header), len(header) + 1}
            and not any(row[:date_index + 1])
            and any(row[date_index + 1:])
        ):
            groups.append(row[:len(header)])

    labels = []
    ancestors = [''] * len(groups)
    for cells in zip(*groups):
        populated = [index for index, value in enumerate(cells) if value]
        if not populated:
            labels.append('')
            continue
        last = populated[-1]
        for index in populated:
            ancestors[index] = cells[index]
            ancestors[index + 1:] = [''] * (len(groups) - index - 1)
        labels.append(' / '.join(filter(None, ancestors[:last + 1])))
    return labels, code_index, chain((first_row,), reader)


def consolidate_reports(
    inputs: dict[str, Path],
    destination: Path,
    raw_root: Path,
    scratch: Path,
) -> None:
    """Publish one table spanning all local months for a report and scope.

    Args:
        inputs: Active originals indexed by their reference month.
        destination: CSV in the interim layer.
        raw_root: Root used to record each row's source path.
        scratch: Directory used to stage the output before publication.
    Returns:
        None.
    Raises:
        IfDataScraperException: An original does not match its reference month.
        OSError: An original could not be read or output could not be saved.
        ValueError: A CSV lacks the required identifier columns.
        csv.Error: A source CSV could not be parsed.
    """
    if not inputs:
        return

    # Identify columns by label and occurrence so duplicates stay distinct.
    files = sorted(inputs.items())
    output_columns: dict[tuple[str, int], int] = {}
    layouts = {}
    for period, path in files:
        validate_report_csv(path, f'{period[5:]}/{period[:4]}')
        with path.open(encoding='utf-8-sig', newline='') as source:
            labels, _, _ = _read_layout(source)
        occurrences: Counter[str] = Counter()
        columns = []
        for label in labels:
            occurrences[label] += 1
            key = (label, occurrences[label])
            columns.append(
                output_columns.setdefault(key, len(output_columns)),
            )
        layouts[period] = columns

    headers = ['data_base', 'arquivo_origem']
    used = set(headers)
    for label, occurrence in output_columns:
        base = label or 'Coluna sem título'
        name = base if occurrence == 1 else f'{base} [{occurrence}]'
        suffix = 2
        while name in used:
            name = f'{base} [{suffix}]'
            suffix += 1
        headers.append(name)
        used.add(name)

    destination.parent.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=scratch) as temporary:
        stage = Path(temporary) / destination.name
        with stage.open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.writer(stream, delimiter=';')
            writer.writerow(headers)
            for period, path in files:
                columns = layouts[period]
                origin = path.relative_to(raw_root).as_posix()
                with path.open(encoding='utf-8-sig', newline='') as source:
                    _, code_index, rows = _read_layout(source)
                    for row in rows:
                        if len(row) <= code_index or not (
                            INSTITUTION_CODE.fullmatch(row[code_index].strip())
                        ):
                            continue
                        values = [''] * len(output_columns)
                        for column, value in zip(columns, row):
                            values[column] = value
                        writer.writerow([period, origin, *values])
        move_artifact(stage, destination, replace=True)
    logger.info(f'Consolidated {len(files)} periods in {destination}.')
