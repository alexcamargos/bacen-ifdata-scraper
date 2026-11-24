"""Type the current portal's observed fields without assuming equivalence.

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

import polars as pl

from bacen_ifdata.scraper.storage.processing import move_artifact

NUMBER = r'^[+-]?(?:[0-9]+|[0-9]{1,3}(?:\.[0-9]{3})+)(?:,[0-9]+)?%?$'


def transform_current_report(
    source: Path, destination: Path, institution: str, report: str,
    scratch: Path,
) -> None:
    """Write one typed Parquet observation per published field and row.

    Args:
        source: Normalized semicolon-delimited CSV.
        destination: Typed period file.
        institution: Stable institutional scope identifier.
        report: Stable report identifier.
        scratch: Location for the temporary Parquet before publication.
    Returns:
        None.
    Raises:
        OSError: A local file could not be read or written.
        ValueError: The cleaned CSV is missing a required identifier.
        PolarsError: The cleaned data could not be typed.
    """
    with source.open(encoding='utf-8', newline='') as stream:
        labels = next(csv.reader(stream, delimiter=';'), [])
    names = [label.strip().casefold() for label in labels]
    aliases = [f'c{index}' for index in range(len(labels))]
    identity = {
        names.index('arquivo_origem'): 'arquivo_origem',
        names.index('instituição'): 'instituicao',
        names.index('código'): 'codigo',
        names.index('data'): 'data_base',
    }
    fields = [index for index in range(len(labels)) if index not in identity]
    date_index = names.index('data')
    dictionary = pl.DataFrame({
        'coluna': [aliases[index] for index in fields],
        'ordem_coluna': [index for index in fields],
        'campo_original': [labels[index] for index in fields],
        'eh_dimensao': [index < date_index for index in fields],
    })
    frame = pl.read_csv(
        source, separator=';', has_header=False, skip_rows=1,
        new_columns=aliases, infer_schema=False,
    ).rename({
        aliases[index]: name for index, name in identity.items()
    }).with_row_index('linha', offset=1)
    value = pl.col('valor_original').str.strip_chars()
    numeric = value.str.contains(NUMBER)
    measurement = numeric & ~pl.col('eh_dimensao')
    typed = (
        frame.unpivot(
            on=[aliases[index] for index in fields],
            index=['linha', *identity.values()],
            variable_name='coluna', value_name='valor_original',
        )
        .join(dictionary, on='coluna', validate='m:1')
        .with_columns(
            pl.lit(institution).alias('escopo'),
            pl.lit(report).alias('relatorio'),
            pl.col('codigo').str.strip_chars(),
            (pl.lit('01/') + pl.col('data_base').str.strip_chars())
            .str.strptime(pl.Date, '%d/%m/%Y').alias('data_base'),
            pl.when(measurement).then(
                value.str.replace_all(r'[.%]', '')
                .str.replace(',', '.')
                .cast(pl.Decimal(precision=38, scale=8), strict=False)
            ).alias('valor_numerico'),
            pl.when(measurement & value.str.ends_with('%'))
            .then(pl.lit('percentual')).alias('formato_valor'),
        )
        .drop('coluna')
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=scratch) as temporary:
        stage = Path(temporary) / destination.name
        typed.write_parquet(stage)
        move_artifact(stage, destination, replace=True)
