"""Tests for Financial Conglomerates Portfolio Geographic Region data transformation schema."""

from pathlib import Path

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.portfolio_geographic_region import (
    FinancialConglomeratePortfolioGeographicRegionSchema,
)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


def test_financial_conglomerates_portfolio_geographic_region_schema_structure():
    """Test that the Financial Conglomerates Portfolio Geographic Region
    schema has correct column names and transformation types.
    """

    schema = FinancialConglomeratePortfolioGeographicRegionSchema()

    expected_structure = {
        'instituicao': TransformationType.TEXT,
        'codigo': TransformationType.NUMERIC,
        'consolidado_bancario': TransformationType.CATEGORICAL,
        'tipo_de_consolidacao': TransformationType.CATEGORICAL,
        'tipo_de_controle': TransformationType.CATEGORICAL,
        'segmento_resolucao': TransformationType.CATEGORICAL,
        'segmento': TransformationType.CATEGORICAL,
        'cidade': TransformationType.TEXT,
        'uf': TransformationType.CATEGORICAL,
        'data_base': TransformationType.DATE,
        'total_geral': TransformationType.NUMERIC,
        'sudeste': TransformationType.NUMERIC,
        'centro_oeste': TransformationType.NUMERIC,
        'nordeste': TransformationType.NUMERIC,
        'norte': TransformationType.NUMERIC,
        'sul': TransformationType.NUMERIC,
        'regiao_nao_informada': TransformationType.NUMERIC,
        'total_exterior': TransformationType.NUMERIC,
    }

    assert set(schema.column_names) == set(expected_structure.keys())

    for column, expected_type in expected_structure.items():
        assert schema.get_type(column) == expected_type


def test_financial_conglomerates_portfolio_geographic_region_transform_integration(
    mocker,
    mock_financial_conglomerates_portfolio_geographic_region_csv_data,
    transformer_factory,
    mock_dataframe_from_csv,
):
    """Should transform Financial Conglomerates Portfolio Geographic Region data correctly."""

    # Create mock DataFrame using the shared helper
    schema = FinancialConglomeratePortfolioGeographicRegionSchema()
    mock_df = mock_dataframe_from_csv(mock_financial_conglomerates_portfolio_geographic_region_csv_data, schema)
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
