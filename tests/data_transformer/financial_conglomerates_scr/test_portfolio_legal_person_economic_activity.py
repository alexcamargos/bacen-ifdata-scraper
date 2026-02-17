from pathlib import Path

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.data_transformer.schemas.financial_conglomerates_scr.portfolio_legal_person_economic_activity import (
    FinancialConglomerateSCRPortfolioLegalPersonEconomicActivitySchema,
)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


def test_financial_conglomerates_scr_portfolio_legal_person_economic_activity_schema_structure():
    """Test that the Financial Conglomerates SCR Portfolio Legal Person Economic Activity schema
    has correct column names and transformation types.
    """

    schema = FinancialConglomerateSCRPortfolioLegalPersonEconomicActivitySchema()

    # Shared categories structure
    categories = [
        'administracao_publica',
        'agricultura',
        'atividade_imobiliaria',
        'comercio',
        'construcao',
        'industrias_extrativas',
        'industrias_de_transformacao',
        'outros',
        'producao_e_distribuicao_de_eletricidade_gas_e_agua',
        'servicos',
        'transporte',
    ]

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
        'regiao': TransformationType.CATEGORICAL,
        'data_base': TransformationType.DATE,
        'total_da_carteira_de_pessoa_juridica': TransformationType.NUMERIC,
    }

    # Add buckets for each category
    for category in categories:
        expected_structure.update(
            {
                f'{category}_vencido_a_partir_15_dias': TransformationType.NUMERIC,
                f'{category}_a_vencer_ate_90_dias': TransformationType.NUMERIC,
                f'{category}_a_vencer_de_91_ate_360_dias': TransformationType.NUMERIC,
                f'{category}_a_vencer_de_361_ate_1080_dias': TransformationType.NUMERIC,
                f'{category}_a_vencer_de_1081_ate_1800_dias': TransformationType.NUMERIC,
                f'{category}_a_vencer_de_1801_ate_5400_dias': TransformationType.NUMERIC,
                f'{category}_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
                f'{category}_total': TransformationType.NUMERIC,
            }
        )

    # Add remaining fields
    expected_structure.update(
        {
            'total_exterior_pessoa_juridica': TransformationType.NUMERIC,
            'atividade_nao_informada': TransformationType.NUMERIC,
            'total_nao_individualizado_pessoa_juridica': TransformationType.NUMERIC,
        }
    )

    assert set(schema.column_names) == set(expected_structure.keys())

    for column, expected_type in expected_structure.items():
        assert schema.get_type(column) == expected_type


def test_financial_conglomerates_scr_portfolio_legal_person_economic_activity_transform_integration(
    mocker,
    mock_financial_conglomerates_scr_portfolio_legal_person_economic_activity_csv_data,
    transformer_factory,
    mock_dataframe_from_csv,
):
    """Should transform Financial Conglomerates SCR Portfolio Legal Person Economic Activity data correctly."""

    # Create mock DataFrame using the shared helper
    schema = FinancialConglomerateSCRPortfolioLegalPersonEconomicActivitySchema()
    mock_df = mock_dataframe_from_csv(
        mock_financial_conglomerates_scr_portfolio_legal_person_economic_activity_csv_data, schema
    )
    mocker.patch('bacen_ifdata.data_transformer.controller.load_csv_data', return_value=mock_df)

    # Use the shared transformer factory fixture
    controller = TransformerController(transformer_factory)

    result = controller.transform(
        file_path=Path("dummy.csv"), schema=schema, institution=Institutions.FINANCIAL_CONGLOMERATES_SCR
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
