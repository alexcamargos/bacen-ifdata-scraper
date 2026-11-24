"""Verify lossless cleaning, typing and period replacement for 2025 exports.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

from datetime import date
from decimal import Decimal
from pathlib import Path

import duckdb
import pytest

from bacen_ifdata.data_cleaner.current import clean_current_report
from bacen_ifdata.data_loader.current import TABLE, replace_current_period
from bacen_ifdata.data_transformer.current import transform_current_report


def test_current_pipeline_preserves_native_fields_and_replaces_only_one_period(
    tmp_path: Path,
) -> None:
    """Keep grouped and textual observations alongside typed numeric values.

    Args:
        tmp_path: Isolated files for both report periods.
    Returns:
        None.
    Raises:
        OSError: A local artifact could not be read or written.
    """
    root = tmp_path / 'raw'
    root.mkdir()
    scratch = tmp_path / 'scratch'
    institution = 'prudential_conglomerates'
    report = 'assets'
    cleaned = tmp_path / 'period.csv'
    typed = tmp_path / 'period.parquet'
    with duckdb.connect() as connection:
        for month in (3, 6, 3):
            period = date(2025, month, 1)
            source = root / f'2025-{month:02}.csv'
            source.write_text(
                'Instituição;Código;TC;Data;Crédito;;Índice;Outro;\n'
                ';;;;Saldo;Perda esperada;;;\n'
                f'Banco;001;2;{month:02}/2025;1.234,50;NI;8,25%;\n'
                f'Total;;2;{month:02}/2025;1.234,50;NI;8,25%;\n',
                encoding='utf-8',
            )
            clean_current_report(
                source, cleaned, period.isoformat()[:7], root, scratch,
            )
            transform_current_report(
                cleaned, typed, institution, report, scratch,
            )
            connection.begin()
            rows = replace_current_period(
                connection, typed, institution, report, period,
            )
            connection.commit()
            assert rows == 5
        assert connection.sql(f'SELECT count(*) FROM {TABLE}').fetchone() == (
            10,
        )
        data = connection.execute(
            f'SELECT campo_original, valor_original, valor_numerico, '
            f'formato_valor, codigo FROM {TABLE} WHERE data_base = ? '
            'ORDER BY ordem_coluna',
            [date(2025, 3, 1)],
        ).fetchall()
        assert data == [
            ('TC', '2', None, None, '001'),
            ('Crédito / Saldo', '1.234,50', Decimal('1234.50'), None, '001'),
            ('Crédito / Perda esperada', 'NI', None, None, '001'),
            ('Índice', '8,25%', Decimal('8.25'), 'percentual', '001'),
            ('Outro', None, None, None, '001'),
        ]
        connection.begin()
        with pytest.raises(ValueError, match='Invalid current report'):
            replace_current_period(
                connection, typed, institution, report, date(2025, 6, 1),
            )
        connection.rollback()
        assert connection.sql(f'SELECT count(*) FROM {TABLE}').fetchone() == (
            10,
        )
