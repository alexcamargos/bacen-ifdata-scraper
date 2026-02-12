"""Tests for Prudential Conglomerate Capital Information data transformation schema."""

from pathlib import Path

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.capital_information import (
    PrudentialConglomerateCapitalInformationSchema,
)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


def test_prudential_conglomerate_capital_information_schema_structure():
    """Test that the Prudential Conglomerate Capital Information schema has correct column names and transformation types."""

    schema = PrudentialConglomerateCapitalInformationSchema()

    expected_structure = {
        'instituicao': TransformationType.TEXT,
        'codigo': TransformationType.NUMERIC,
        'consolidado_bancario': TransformationType.CATEGORICAL,
        'segmento_resolucao': TransformationType.CATEGORICAL,
        'tcip': TransformationType.CATEGORICAL,
        'tipo_de_consolidacao': TransformationType.CATEGORICAL,
        'tipo_de_controle': TransformationType.CATEGORICAL,
        'cidade': TransformationType.TEXT,
        'uf': TransformationType.CATEGORICAL,
        'regiao': TransformationType.CATEGORICAL,
        'data_base': TransformationType.DATE,
        'capital_principal_para_comparacao_com_rwa': TransformationType.NUMERIC,
        'capital_complementar': TransformationType.NUMERIC,
        'patrimonio_referencia_nivel_i_para_comparacao_com_rwa': TransformationType.NUMERIC,
        'capital_nivel_ii': TransformationType.NUMERIC,
        'patrimonio_referencia_para_comparacao_com_rwa': TransformationType.NUMERIC,
        'rwa_risco_credito': TransformationType.NUMERIC,
        'rwacam': TransformationType.NUMERIC,
        'rwacom': TransformationType.NUMERIC,
        'rwajur': TransformationType.NUMERIC,
        'rwaacs': TransformationType.NUMERIC,
        'rwacva': TransformationType.NUMERIC,
        'rwadrc': TransformationType.NUMERIC,
        'rwa_risco_mercado': TransformationType.NUMERIC,
        'rwa_risco_operacional': TransformationType.NUMERIC,
        'rwasp': TransformationType.NUMERIC,
        'ativos_ponderados_pelo_risco_rwa': TransformationType.NUMERIC,
        'exposicao_total': TransformationType.NUMERIC,
        'indice_capital_principal': TransformationType.PERCENTAGE,
        'indice_capital_nivel_i': TransformationType.PERCENTAGE,
        'indice_basileia': TransformationType.PERCENTAGE,
        'adicional_capital_principal': TransformationType.NUMERIC,
        'razao_alavancagem': TransformationType.PERCENTAGE,
        'indice_imobilizacao': TransformationType.PERCENTAGE,
    }

    assert set(schema.column_names) == set(expected_structure.keys())

    for column, expected_type in expected_structure.items():
        assert schema.get_type(column) == expected_type


def test_prudential_conglomerate_capital_information_transform_integration(
    mocker, mock_prudential_conglomerate_capital_information_csv_data, transformer_factory, mock_dataframe_from_csv
):
    """Should transform Prudential Conglomerate Capital Information data correctly."""

    # Create mock DataFrame using the shared helper
    schema = PrudentialConglomerateCapitalInformationSchema()
    mock_df = mock_dataframe_from_csv(mock_prudential_conglomerate_capital_information_csv_data, schema)
    mocker.patch('bacen_ifdata.data_transformer.controller.load_csv_data', return_value=mock_df)

    # Use the shared transformer factory fixture
    controller = TransformerController(transformer_factory)

    result = controller.transform(
        file_path=Path("dummy.csv"), schema=schema, institution=Institutions.PRUDENTIAL_CONGLOMERATES
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
