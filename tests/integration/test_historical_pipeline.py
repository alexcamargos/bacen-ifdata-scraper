"""Check preservation and period validation for historical IF.data exports.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

import csv
from datetime import date
from decimal import Decimal
from enum import StrEnum
from pathlib import Path

import duckdb
import pytest
from pytest_mock import MockerFixture

from bacen_ifdata import Pipeline
from bacen_ifdata.data_cleaner.processing import normalize_csv
from bacen_ifdata.data_loader.storage import DatabaseService
from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.data_transformer.schemas.mapper import (
    SCHEMA_BY_INSTITUTION_AND_REPORT,
)
from bacen_ifdata.data_transformer.transformer_factory import get_transformer
from bacen_ifdata.manager import PipelineManager
from bacen_ifdata.scraper.institutions import InstitutionType
from bacen_ifdata.scraper.reports import (
    ReportsFinancialConglomerates,
    ReportsFinancialConglomeratesSCR,
    ReportsForeignExchange,
    ReportsPrudentialConglomerates,
)
from bacen_ifdata.scraper.storage.collection import report_inputs
from bacen_ifdata.updates import _inventory
from bacen_ifdata.utilities.configurations import Config


@pytest.mark.transformation
@pytest.mark.parametrize(
    ('scope', 'report', 'month', 'columns'),
    [
        (
            InstitutionType.FOREIGN_EXCHANGE,
            ReportsForeignExchange.QUARTERLY_FOREIGN_CURRENCY_FLOW,
            '2023-06',
            {
                'operacoes_comerciais_compra_numero_operacoes': 9,
                'operacoes_comerciais_compra_valor': 10,
                'operacoes_comerciais_venda_valor': 12,
                'operacoes_financeiras_compra_valor': 16,
                'mercado_interbancario_venda_valor': 26,
                'total_geral_valor': 30,
            },
        ),
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            ReportsPrudentialConglomerates.CAPITAL_INFORMATION,
            '2015-03',
            {
                'capital_principal_para_comparacao_com_rwa': 9,
                'rwa_risco_credito': 14,
                'ativos_ponderados_pelo_risco_rwa': 21,
                'indice_basileia': 25,
            },
        ),
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            ReportsPrudentialConglomerates.CAPITAL_INFORMATION,
            '2024-12',
            {
                'capital_principal_para_comparacao_com_rwa': 10,
                'rwa_risco_credito': 15,
                'ativos_ponderados_pelo_risco_rwa': 25,
                'indice_basileia': 29,
                'adicional_capital_principal': 30,
            },
        ),
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            ReportsPrudentialConglomerates.SEGMENTATION,
            '2024-12',
            {
                'exposicao_total_ou_ativo_total': 11,
                'total_ativos_consolidados_exterior': 12,
            },
        ),
        (
            InstitutionType.FINANCIAL_CONGLOMERATES,
            ReportsFinancialConglomerates.CAPITAL_INFORMATION,
            '2014-12',
            {
                'patrimonio_referencia_nivel_i_para_comparacao_com_rwa': 11,
                'patrimonio_referencia_para_comparacao_com_rwa': 13,
                'rwa_risco_credito': 14,
                'ativos_ponderados_pelo_risco_rwa': 21,
            },
        ),
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            ReportsPrudentialConglomerates.SUMMARY,
            '2024-12',
            {'patrimonio_de_referencia': 15},
        ),
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            ReportsPrudentialConglomerates.INCOME_STATEMENT,
            '2024-12',
            {
                'rendas_operacoes_de_credito': 9,
                'resultado_intermediacao_financeira': 22,
            },
        ),
        (
            InstitutionType.FINANCIAL_CONGLOMERATES_SCR,
            ReportsFinancialConglomeratesSCR
            .PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY,
            '2012-06',
            {
                'operacoes_com_recebiveis_vencido_a_partir_15_dias': 35,
                'operacoes_com_recebiveis_a_vencer_ate_90_dias': 36,
                'operacoes_com_recebiveis_a_vencer_de_91_ate_360_dias': 37,
                'comercio_exterior_vencido_a_partir_15_dias': 43,
                'comercio_exterior_a_vencer_de_91_ate_360_dias': 45,
                'outros_creditos_vencido_a_partir_15_dias': 51,
                'outros_creditos_a_vencer_de_361_ate_1080_dias': 54,
            },
        ),
    ],
)
def test_historical_measures_reach_silver(
    tmp_path: Path,
    scope: InstitutionType,
    report: StrEnum,
    month: str,
    columns: dict[str, int],
) -> None:
    """Compare real source positions with the values stored in DuckDB.

    Args:
        tmp_path: Temporary working directory for normalized and typed CSVs.
        scope: Institutional scope of the export.
        report: Report to transform and load.
        month: Reference month of the source export.
        columns: Silver field names and independent source CSV positions.
    Returns:
        None.
    Raises:
        OSError: The source export could not be opened or normalized.
    """
    directory = Config.DOWNLOAD_DIRECTORY / scope.name.lower()
    source = report_inputs(directory / report.name.lower()).get(month)
    if source is None:
        pytest.skip(
            f'Original IF.data export unavailable: {report.name}/{month}'
        )

    with source.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.reader(stream, delimiter=';')
        header = next(reader)
        code_index = header.index('Código')
        row = next(
            row for row in reader
            if len(row) > code_index
            and row[code_index].replace('.', '').isdigit()
        )

    schema = SCHEMA_BY_INSTITUTION_AND_REPORT[scope][report]
    cleaned, typed = tmp_path / 'cleaned.csv', tmp_path / 'typed.csv'
    assert normalize_csv(
        scope, report, source.name, source=source, destination=cleaned,
    )
    transformer = TransformerController(get_transformer)
    transformer.transform(cleaned, schema, scope).to_csv(typed, index=False)

    with duckdb.connect() as connection:
        database = DatabaseService(connection=connection)
        with database.transaction():
            database.create_table('report', schema)
            database.replace_period(
                'report', typed, schema, date.fromisoformat(f'{month}-01'),
                source=source,
            )
        fields = ', '.join(columns)
        values = connection.execute(
            f'SELECT {fields} FROM report WHERE codigo = ?',
            [int(row[code_index].replace('.', ''))],
        ).fetchone()

    assert values is not None
    for (name, position), actual in zip(columns.items(), values, strict=True):
        raw = row[position].replace('.', '').replace(',', '.')
        expected = Decimal(raw.rstrip('%'))
        if raw.endswith('%'):
            expected /= 100
        assert actual == pytest.approx(float(expected)), name


@pytest.mark.parametrize(
    'invalid_rows',
    ['Outra data,101,2024-09-01\n', 'A,101,2024-12-01\nB,101,2024-12-01\n'],
)
def test_manual_load_rolls_back_a_bad_historical_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, invalid_rows: str,
) -> None:
    """Keep the previous warehouse if a batch contains a bad period.

    Args:
        tmp_path: Isolated warehouse and CSV root.
        monkeypatch: Fixture used to point the loader at the test CSVs.
        invalid_rows: CSV data that violates the date or unique code rule.
    Returns:
        None.
    Raises:
        OSError: The fixture files cannot be created.
    """
    institution = InstitutionType.FINANCIAL_CONGLOMERATES
    report = ReportsFinancialConglomerates.SUMMARY
    table = 'financial_conglomerates_summary'
    typed = tmp_path / institution.name.lower() / report.name.lower()
    typed.mkdir(parents=True)
    monkeypatch.setattr(Config, 'TRANSFORMED_FILES_DIRECTORY', tmp_path)
    header = 'instituicao,codigo,data_base\n'
    (typed / '2024-09.csv').write_text(
        header + 'Válido,101,2024-09-01\n', encoding='utf-8',
    )
    (typed / '2024-12.csv').write_text(
        header + invalid_rows, encoding='utf-8',
    )

    with duckdb.connect() as connection:
        connection.execute(f'CREATE TABLE {table} AS SELECT 999 AS codigo')
        manager = PipelineManager(
            Pipeline(TransformerController(get_transformer)),
            database_service=DatabaseService(connection=connection),
        )
        with pytest.raises(ValueError, match='2024-12.csv.*data-base 2024-12'):
            manager.run_loader(institution.name, report.name)
        assert connection.execute(f'SELECT codigo FROM {table}').fetchall() == [
            (999,)
        ]


def test_inventory_excludes_periods_after_2024(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture,
) -> None:
    """Exclude out-of-scope originals before reading their contents.

    Args:
        tmp_path: Isolated raw directory root.
        monkeypatch: Fixture used to point the inventory at the test originals.
        mocker: Fixture used to observe calls to the checksum operation.
    Returns:
        None.
    Raises:
        OSError: The fixture files cannot be created.
    """
    directory = tmp_path / 'financial_conglomerates' / 'summary'
    directory.mkdir(parents=True)
    included = directory / '2024-12.csv'
    included.write_text('Included', encoding='utf-8')
    (directory / '2025-03.csv').write_text('Excluded', encoding='utf-8')
    monkeypatch.setattr(Config, 'DOWNLOAD_DIRECTORY', tmp_path)
    checksum = mocker.patch(
        'bacen_ifdata.updates.report_checksum', return_value='digest',
    )

    inputs = _inventory()

    assert [entry.period for entry in inputs.values()] == [date(2024, 12, 1)]
    checksum.assert_called_once_with(included)
