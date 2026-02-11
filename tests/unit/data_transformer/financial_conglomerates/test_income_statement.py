"""Tests for Financial Conglomerates Income Statement data transformation schema."""

from pathlib import Path

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.income_statement import (
    FinancialConglomerateIncomeStatementSchema,
)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


def test_financial_conglomerates_income_statement_schema_structure():
    """Deve ter os nomes das colunas e tipos corretos definidos."""
    schema = FinancialConglomerateIncomeStatementSchema()

    expected_structure = {
        'instituicao': TransformationType.TEXT,
        'codigo': TransformationType.NUMERIC,
        'consolidado_bancario': TransformationType.CATEGORICAL,
        'segmento_resolucao': TransformationType.CATEGORICAL,
        'tipo_de_consolidacao': TransformationType.CATEGORICAL,
        'tipo_de_controle': TransformationType.CATEGORICAL,
        'cidade': TransformationType.TEXT,
        'uf': TransformationType.CATEGORICAL,
        'data_base': TransformationType.DATE,
        'rendas_operacoes_de_credito': TransformationType.NUMERIC,
        'rendas_operacoes_de_arrendamento_mercantil': TransformationType.NUMERIC,
        'rendas_operacoes_tvm': TransformationType.NUMERIC,
        'rendas_operacoes_instrumentos_financeiros_derivativos': TransformationType.NUMERIC,
        'resultado_operacoes_cambio': TransformationType.NUMERIC,
        'rendas_aplicacoes_compulsorias': TransformationType.NUMERIC,
        'receitas_intermediacao_financeira': TransformationType.NUMERIC,
        'despesas_captacao': TransformationType.NUMERIC,
        'despesas_obrigacoes_emprestimos_repasses': TransformationType.NUMERIC,
        'despesas_operacoes_arrendamento_mercantil': TransformationType.NUMERIC,
        'despesas_operacoes_cambio': TransformationType.NUMERIC,
        'resultado_provisao_creditos_dificil_liquidacao': TransformationType.NUMERIC,
        'despesas_intermediacao_financeira': TransformationType.NUMERIC,
        'resultado_intermediacao_financeira': TransformationType.NUMERIC,
        'rendas_prestacao_servicos': TransformationType.NUMERIC,
        'rendas_tarifas_bancarias': TransformationType.NUMERIC,
        'despesas_pessoal': TransformationType.NUMERIC,
        'despesas_administrativas': TransformationType.NUMERIC,
        'despesas_tributarias': TransformationType.NUMERIC,
        'resultado_participacoes': TransformationType.NUMERIC,
        'outras_receitas_operacionais': TransformationType.NUMERIC,
        'outras_despesas_operacionais': TransformationType.NUMERIC,
        'outras_receitas_despesas_operacionais': TransformationType.NUMERIC,
        'resultado_operacional': TransformationType.NUMERIC,
        'resultado_nao_operacional': TransformationType.NUMERIC,
        'resultado_antes_tributacao_lucro_participacao': TransformationType.NUMERIC,
        'imposto_renda_contribuicao_social': TransformationType.NUMERIC,
        'participacao_lucros': TransformationType.NUMERIC,
        'lucro_liquido': TransformationType.NUMERIC,
        'juros_sobre_capital_social_cooperativas': TransformationType.NUMERIC,
    }

    assert set(schema.column_names) == set(expected_structure.keys())

    for column, expected_type in expected_structure.items():
        assert schema.get_type(column) == expected_type


def test_financial_conglomerates_income_statement_transform_integration(
    mocker, mock_financial_conglomerates_income_statement_csv_data, transformer_factory, mock_dataframe_from_csv
):
    """Should transform Financial Conglomerates Income Statement data correctly."""

    # Create mock DataFrame using the shared helper
    schema = FinancialConglomerateIncomeStatementSchema()
    mock_df = mock_dataframe_from_csv(mock_financial_conglomerates_income_statement_csv_data, schema)
    mocker.patch('bacen_ifdata.data_transformer.controller.load_csv_data', return_value=mock_df)

    # Use the shared transformer factory fixture
    controller = TransformerController(transformer_factory)

    result = controller.transform(
        file_path=Path("dummy.csv"), schema=schema, institution=Institutions.FINANCIAL_CONGLOMERATES
    )

    # Verify transformation
    assert isinstance(result, pd.DataFrame)
    # Ensure the mock data resulted in exactly 2 records as expected from the input fixture.
    assert len(result) == 2
    # Check that all expected columns are present in the result.
    assert all(column in result.columns for column in schema.column_names)
    # Validate that the data types of the transformed columns match the expected types defined in the schema.
    for column in schema.column_names:
        expected_type = schema.get_type(column)
        if expected_type in (TransformationType.TEXT, TransformationType.CATEGORICAL):
            assert pd.api.types.is_object_dtype(result[column]) or pd.api.types.is_string_dtype(result[column])
        elif expected_type in (TransformationType.NUMERIC, TransformationType.PERCENTAGE):
            assert pd.api.types.is_numeric_dtype(result[column])
        elif expected_type == TransformationType.DATE:
            assert pd.api.types.is_datetime64_any_dtype(result[column])
