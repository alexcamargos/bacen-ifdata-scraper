"""Compare populated IF.data source measures with the published Silver.

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
from collections import defaultdict
from collections.abc import Iterator
from datetime import date
from hashlib import sha256
from io import StringIO
from itertools import chain, islice
from pathlib import Path
from tempfile import TemporaryDirectory

import duckdb
import pandas as pd
import polars as pl
from loguru import logger

from bacen_ifdata.data_cleaner.processing import _process_csv_header
from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.data_transformer.schemas.interfaces import SchemaProtocol
from bacen_ifdata.data_transformer.schemas.mapper import (
    SCHEMA_BY_INSTITUTION_AND_REPORT,
)
from bacen_ifdata.data_transformer.transformer_factory import get_transformer
from bacen_ifdata.scraper.storage.collection import INSTITUTION_CODE
from bacen_ifdata.scraper.storage.processing import move_artifact
from bacen_ifdata.updates import RawInput, _applied_inputs, _inventory
from bacen_ifdata.utilities.configurations import Config
from bacen_ifdata.utilities.releases import current_release
from bacen_ifdata.utilities.string_utils import slugify

IDENTIFIERS = {
    'codigo', 'conglomerado_financeiro', 'conglomerado_prudencial',
}
MEASURE_TYPES = {'integer', 'numeric', 'percentage'}
# Historical IF.data measures use NI and NI% as well as NA and NA%.
MISSING = {'', '-', 'na', 'na%', 'n/a', 'nan', 'ni', 'ni%', 'null', 'none'}
NUMBER = re.compile(
    r'[+-]?(?:[0-9]+|[0-9]{1,3}(?:\.[0-9]{3})+)(?:,[0-9]+)?\s*%?'
)
CoverageRow = dict[str, str | int | date | None]


def _original_columns(path: Path) -> tuple[str, dict[str, tuple[str, ...]]]:
    """Read original values and identify the full multirow layout.

    Args:
        path: Active Bronze export with the IF.data header and footers.
    Returns:
        The layout SHA-256 and source values by normalized header name.
    Raises:
        OSError: The original cannot be opened.
        ValueError: The header or an institution row has invalid structure.
        csv.Error: A CSV record cannot be read.
    """
    with path.open(encoding='utf-8-sig') as stream:
        prefix = list(islice(stream, 6))
        if not prefix:
            raise ValueError(f'{path}: empty original.')
        header, start = _process_csv_header(prefix)
        if header[-1] in ('', '\n'):
            header.pop()
        names = pd.read_csv(
            StringIO(';'.join(header)), sep=';', nrows=0,
        ).columns.tolist()
        canonical_names = [slugify(name) for name in names]
        if 'codigo' not in canonical_names:
            raise ValueError(f'{path}: missing Código in the original.')
        code = canonical_names.index('codigo')
        rows = []
        for row in csv.reader(chain(prefix[start:], stream), delimiter=';'):
            if len(row) <= code or not INSTITUTION_CODE.fullmatch(
                row[code].strip()
            ):
                continue
            if len(row) == len(names) + 1 and not row[-1]:
                row.pop()
            if len(row) != len(names):
                raise ValueError(f'{path}: invalid institution row width.')
            rows.append(row)

    original_headers = list(csv.reader(prefix[:start], delimiter=';'))
    layout = sha256(
        json.dumps(original_headers, ensure_ascii=False).encode('utf-8')
    ).hexdigest()
    values = zip(*rows, strict=True) if rows else [()] * len(names)
    return layout, dict(zip(names, values, strict=True))


def _compare_export(
    entry: RawInput,
    schema: SchemaProtocol,
    measures: list[str],
    transformer: TransformerController,
    silver: dict[str, int | None] | None,
) -> Iterator[CoverageRow]:
    """Yield field coverage records for one original and its Silver period.

    Args:
        entry: Original input and Bronze lineage.
        schema: Canonical layout of this report.
        measures: Canonical fields considered measures.
        transformer: The controller used for resolving historical aliases.
        silver: Populated Silver counts for the same original or None.
            A None value for a measure means its Silver column is absent.
    Yields:
        One record per measure and per unmapped numeric source column.
    Returns:
        None.
    Raises:
        OSError: The original cannot be opened.
        ValueError: The original's structure cannot be audited.
        csv.Error: A CSV record cannot be read.
    """
    layout, columns = _original_columns(entry.path)
    rename = transformer._build_column_rename_map(
        pd.DataFrame(columns=list(columns)), schema,
    )
    input_fields = set(schema.input_column_names)
    mapped = {
        rename.get(header, header): header for header in columns
        if rename.get(header, header) in input_fields
    }
    _, institution, report, month = entry.key
    common = {
        'instituicao': institution, 'relatorio': report, 'data_base': month,
        'leiaute_sha256': layout, 'arquivo_origem': str(entry.path),
        'sha256_origem': entry.checksum,
        'linhas_origem': len(next(iter(columns.values()))),
        'linhas_silver': silver.get('linhas_silver') if silver else None,
    }
    for measure in measures:
        header = mapped.get(measure)
        source_count = non_numeric = None
        if header is not None:
            source_count = non_numeric = 0
            for value in columns[header]:
                token = value.strip()
                if token.casefold() in MISSING:
                    continue
                if NUMBER.fullmatch(token):
                    source_count += 1
                else:
                    non_numeric += 1
        silver_count = silver[measure] if silver is not None else None
        if silver is None:
            status = 'silver_sem_mesmo_original'
        elif silver_count is None:
            status = 'medida_ausente_na_silver'
        elif header is None:
            status = 'sem_cabecalho_mapeado'
        elif source_count != silver_count:
            status = 'contagem_divergente'
        elif non_numeric:
            status = 'texto_na_medida_de_origem'
        elif source_count == 0:
            status = 'sem_valores_na_origem'
        else:
            status = 'coberta'
        yield {
            **common, 'medida': measure, 'cabecalho_origem': header,
            'valores_origem': source_count, 'valores_silver': silver_count,
            'valores_nao_numericos': non_numeric,
            'situacao': status,
        }

    for header in columns.keys() - set(mapped.values()):
        numbers = sum(
            NUMBER.fullmatch(value.strip()) is not None
            for value in columns[header]
        )
        if numbers:
            yield {
                **common, 'medida': None, 'cabecalho_origem': header,
                'valores_origem': numbers, 'valores_silver': None,
                'valores_nao_numericos': None,
                'situacao': 'coluna_numerica_sem_mapeamento',
            }


def audit_measure_coverage(
    institution: str | None = None, report: str | None = None,
) -> Path:
    """Write a read-only Bronze–Silver coverage audit as Parquet in scratch.

    Args:
        institution: Institutional enum name to inspect, if specified.
        report: Report enum name to inspect, if specified.
    Returns:
        Path to the coverage Parquet for the selected reports.
    Raises:
        FileNotFoundError: A published Silver release is required.
        ValueError: The filter has no inputs or an original is malformed.
        OSError: An input cannot be read or the result cannot be written.
        duckdb.Error: The published Silver cannot be queried.
        csv.Error: An original CSV record cannot be read.
    """
    release = current_release(Config.DATA_DIRECTORY)
    if release is None:
        raise FileNotFoundError('A published Silver release is required.')
    inputs = _inventory()
    applied = _applied_inputs(release.silver)
    transformer = TransformerController(get_transformer)
    rows: list[CoverageRow] = []
    with duckdb.connect(str(release.silver), read_only=True) as database:
        published_columns = defaultdict(set)
        for table, name in database.execute(
            'SELECT table_name, column_name FROM information_schema.columns '
            "WHERE table_schema = 'main'"
        ).fetchall():
            published_columns[table].add(name)
        for scope, reports in SCHEMA_BY_INSTITUTION_AND_REPORT.items():
            if institution and scope.name != institution.upper():
                continue
            for report_type, schema in reports.items():
                if report and report_type.name != report.upper():
                    continue
                names = scope.name.lower(), report_type.name.lower()
                entries = [entry for key, entry in inputs.items()
                           if key[1:3] == names]
                if not entries:
                    continue
                measures = [name for name in schema.input_column_names
                            if schema.get_type(name) in MEASURE_TYPES
                            and name not in IDENTIFIERS]
                table = '_'.join(names)
                available = published_columns.get(table, set())
                periods = []
                if available:
                    counts = ''.join(
                        f', count("{name}")' if name in available
                        else ', NULL::BIGINT' for name in measures
                    )
                    periods = database.execute(
                        f'SELECT data_base, count(*){counts} FROM {table} '
                        'GROUP BY data_base'
                    ).fetchall()
                by_period = {
                    period: {
                        'linhas_silver': row_count,
                        **dict(zip(measures, values, strict=True)),
                    }
                    for period, row_count, *values in periods
                }
                for entry in entries:
                    checksum, _ = applied.get(entry.key, (None, None))
                    silver = (
                        by_period.get(entry.period)
                        if checksum == entry.checksum else None
                    )
                    rows.extend(_compare_export(
                        entry, schema, measures, transformer, silver,
                    ))
    if not rows:
        raise ValueError('No original IF.data reports match the filters.')
    suffix = '_'.join(
        value.lower() for value in (institution, report) if value
    )
    name = f'ifdata_measure_coverage_{suffix}.parquet' if suffix else (
        'ifdata_measure_coverage.parquet'
    )
    directory = Config.SCRATCH_DIRECTORY
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / name
    with TemporaryDirectory(dir=directory) as temporary:
        staged = Path(temporary) / name
        coverage = pl.DataFrame(
            rows, infer_schema_length=None,
            schema_overrides={
                'medida': pl.String, 'cabecalho_origem': pl.String,
                'valores_origem': pl.Int64, 'valores_silver': pl.Int64,
                'valores_nao_numericos': pl.Int64,
                'linhas_silver': pl.Int64,
            },
        ).with_columns(
            pl.lit(release.silver.parent.name).alias('release_silver')
        )
        coverage.sort(
            'instituicao', 'relatorio', 'data_base', 'medida',
            'cabecalho_origem',
        ).write_parquet(staged)
        move_artifact(staged, output, replace=True)
    logger.info(f'Coverage audit: {len(rows)} records saved to {output}.')
    return output
