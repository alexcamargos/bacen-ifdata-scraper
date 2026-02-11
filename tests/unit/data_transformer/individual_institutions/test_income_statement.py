"""Tests for the Individual Institutions Income Statement data transformation."""

from pathlib import Path

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.data_transformer.schemas.individual_institutions.income_statement import (
    IndividualInstitutionIncomeStatementSchema,
)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


def test_individual_institutions_income_statement_schema_structure():
    """Test that the Income Statement schema has correct column names and transformation types."""

    schema = IndividualInstitutionIncomeStatementSchema()

    expected_structure = {
        'instituicao': TransformationType.TEXT,
        'codigo': TransformationType.NUMERIC,
        'conglomerado': TransformationType.TEXT,
        'conglomerado_financeiro': TransformationType.NUMERIC,
        'conglomerado_prudencial': TransformationType.NUMERIC,
        'consolidado_bancario': TransformationType.CATEGORICAL,
        'tipo_de_controle': TransformationType.CATEGORICAL,
        'tipo_de_instituicao': TransformationType.CATEGORICAL,
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


def test_individual_institutions_income_statement_transform_integration(
    mocker, mock_individual_institutions_income_statement_csv_data, transformer_factory, mock_dataframe_from_csv
):
    """Should transform Individual Institutions Income Statement data correctly."""

    # Create mock DataFrame using the shared helper
    schema = IndividualInstitutionIncomeStatementSchema()
    mock_df = mock_dataframe_from_csv(mock_individual_institutions_income_statement_csv_data, schema)
    mocker.patch('bacen_ifdata.data_transformer.controller.load_csv_data', return_value=mock_df)

    # Use the shared transformer factory fixture
    controller = TransformerController(transformer_factory)

    result = controller.transform(
        file_path=Path("dummy.csv"), schema=schema, institution=Institutions.INDIVIDUAL_INSTITUTIONS
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
