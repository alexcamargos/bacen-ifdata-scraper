"""Tests for Financial Conglomerates Assets data transformation schema."""

from pathlib import Path

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.assets import FinancialConglomeratesAssetsSchema
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


def test_financial_conglomerates_assets_schema_structure():
    """Test that the Financial Conglomerates Assets schema has correct column names and transformation types."""

    schema = FinancialConglomeratesAssetsSchema()

    expected_structure = {
        'instituicao_financeira': TransformationType.TEXT,
        'codigo': TransformationType.NUMERIC,
        'consolidado_bancario': TransformationType.CATEGORICAL,
        'segmento_resolucao': TransformationType.CATEGORICAL,
        'tipo_de_consolidacao': TransformationType.CATEGORICAL,
        'tipo_de_controle': TransformationType.CATEGORICAL,
        'cidade': TransformationType.TEXT,
        'uf': TransformationType.CATEGORICAL,
        'regiao': TransformationType.CATEGORICAL,
        'data_base': TransformationType.DATE,
        'disponibilidades': TransformationType.NUMERIC,
        'aplicacoes_interfinanceiras_liquidez': TransformationType.NUMERIC,
        'tvm_e_instrumentos_financeiros_derivativos': TransformationType.NUMERIC,
        'operacoes_de_credito': TransformationType.NUMERIC,
        'provisao_operacoes_de_credito': TransformationType.NUMERIC,
        'operacoes_de_credito_liquidas_provisao': TransformationType.NUMERIC,
        'arrendamento_mercantil_a_receber': TransformationType.NUMERIC,
        'imobilizado_de_arrendamento': TransformationType.NUMERIC,
        'credores_antecipacao_valor_residual': TransformationType.NUMERIC,
        'provisao_arrendamento_mercantil': TransformationType.NUMERIC,
        'arrendamento_mercantil_liquido_de_provisao': TransformationType.NUMERIC,
        'outros_creditos_liquido_de_provisao': TransformationType.NUMERIC,
        'outros_ativos_realizaveis': TransformationType.NUMERIC,
        'permanente_ajustado': TransformationType.NUMERIC,
        'ativo_total_ajustado': TransformationType.NUMERIC,
        'credores_antecipacao_valor_residual_j': TransformationType.NUMERIC,
        'ativo_total': TransformationType.NUMERIC,
    }

    # Validate the column names
    assert set(schema.column_names) == set(expected_structure.keys())

    # Validate the types of each column
    for column, expected_type in expected_structure.items():
        assert schema.get_type(column) == expected_type


def test_financial_conglomerates_assets_transform_integration(
    mocker, mock_financial_conglomerates_assets_csv_data, transformer_factory, mock_dataframe_from_csv
):
    """Should transform Financial Conglomerates Assets data correctly."""

    # Create mock DataFrame using the shared helper
    schema = FinancialConglomeratesAssetsSchema()
    mock_df = mock_dataframe_from_csv(mock_financial_conglomerates_assets_csv_data, schema)
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
