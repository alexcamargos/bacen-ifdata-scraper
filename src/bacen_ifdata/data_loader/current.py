"""Store current-layout observations in the DuckDB Silver warehouse.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

from datetime import date
from pathlib import Path

from duckdb import DuckDBPyConnection

TABLE = 'ifdata_2025_campos'


def replace_current_period(
    connection: DuckDBPyConnection, source: Path, institution: str,
    report: str, period: date,
) -> int:
    """Replace one complete current-layout partition in an open transaction.

    Args:
        connection: Silver connection with a transaction owned by the caller.
        source: Typed Parquet source.
        institution: Expected institutional scope.
        report: Expected report identifier.
        period: Reference date expected in every row.
    Returns:
        Number of field observations written.
    Raises:
        ValueError: The typed report is empty or has a different scope or date.
        duckdb.Error: The partition could not be replaced.
    """
    connection.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE} (
            escopo VARCHAR NOT NULL, relatorio VARCHAR NOT NULL,
            data_base DATE NOT NULL, linha BIGINT NOT NULL,
            ordem_coluna INTEGER NOT NULL, codigo VARCHAR NOT NULL,
            instituicao VARCHAR NOT NULL, campo_original VARCHAR NOT NULL,
            eh_dimensao BOOLEAN NOT NULL, valor_original VARCHAR,
            valor_numerico DECIMAL(38,8), formato_valor VARCHAR,
            arquivo_origem VARCHAR NOT NULL
        )
    ''')
    count, matching = connection.execute(
        '''
        SELECT count(*), count(*) FILTER (
            WHERE escopo = ? AND relatorio = ? AND data_base = ?
        ) FROM read_parquet(?)
        ''',
        [institution, report, period, str(source)],
    ).fetchone()
    if not count or count != matching:
        raise ValueError(f'Invalid current report partition: {source}')
    connection.execute(
        f'DELETE FROM {TABLE} WHERE escopo = ? AND relatorio = ? '
        'AND data_base = ?',
        [institution, report, period],
    )
    connection.execute(
        f'INSERT INTO {TABLE} BY NAME SELECT * FROM read_parquet(?)',
        [str(source)],
    )
    return count
