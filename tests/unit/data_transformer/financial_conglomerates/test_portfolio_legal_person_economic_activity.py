"""Tests for Financial Conglomerates Portfolio Legal Person Economic Activity data transformation schema."""

from pathlib import Path

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.portfolio_legal_person_economic_activity import (
    FinancialConglomeratePortfolioLegalPersonEconomicActivitySchema,
)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


def test_financial_conglomerates_portfolio_legal_person_economic_activity_schema_structure():
    """Deve ter os nomes das colunas e tipos corretos definidos."""
    schema = FinancialConglomeratePortfolioLegalPersonEconomicActivitySchema()

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
        'total_carteira_pessoa_juridica': TransformationType.NUMERIC,
        # Agricultura
        'agricultura_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'agricultura_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'agricultura_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'agricultura_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'agricultura_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'agricultura_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'agricultura_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'agricultura_total': TransformationType.NUMERIC,
        # Indústrias de Transformação
        'industrias_transformacao_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'industrias_transformacao_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'industrias_transformacao_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'industrias_transformacao_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'industrias_transformacao_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'industrias_transformacao_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'industrias_transformacao_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'industrias_transformacao_total': TransformationType.NUMERIC,
        # Construção
        'construcao_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'construcao_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'construcao_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'construcao_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'construcao_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'construcao_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'construcao_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'construcao_total': TransformationType.NUMERIC,
        # Serviços Industriais
        'servicos_industriais_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'servicos_industriais_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'servicos_industriais_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'servicos_industriais_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'servicos_industriais_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'servicos_industriais_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'servicos_industriais_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'servicos_industriais_total': TransformationType.NUMERIC,
        # Indústrias Extrativas
        'industrias_extrativas_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'industrias_extrativas_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'industrias_extrativas_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'industrias_extrativas_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'industrias_extrativas_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'industrias_extrativas_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'industrias_extrativas_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'industrias_extrativas_total': TransformationType.NUMERIC,
        # Comércio
        'comercio_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'comercio_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'comercio_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'comercio_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'comercio_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'comercio_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'comercio_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'comercio_total': TransformationType.NUMERIC,
        # Administração Pública
        'administracao_publica_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'administracao_publica_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'administracao_publica_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'administracao_publica_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'administracao_publica_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'administracao_publica_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'administracao_publica_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'administracao_publica_total': TransformationType.NUMERIC,
        # Transporte
        'transporte_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'transporte_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'transporte_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'transporte_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'transporte_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'transporte_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'transporte_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'transporte_total': TransformationType.NUMERIC,
        # Outros
        'outros_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'outros_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'outros_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'outros_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'outros_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'outros_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'outros_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'outros_total': TransformationType.NUMERIC,
        'atividade_nao_informada': TransformationType.NUMERIC,
        'total_nao_individualizado_pessoa_juridica': TransformationType.NUMERIC,
        'total_exterior_pessoa_juridica': TransformationType.NUMERIC,
    }

    assert set(schema.column_names) == set(expected_structure.keys())

    for column, expected_type in expected_structure.items():
        assert schema.get_type(column) == expected_type


def test_financial_conglomerates_portfolio_legal_person_economic_activity_transform_integration(
    mocker,
    mock_financial_conglomerates_portfolio_legal_person_economic_activity_csv_data,
    transformer_factory,
    mock_dataframe_from_csv,
):
    """Should transform Financial Conglomerates Portfolio Legal Person Economic Activity data correctly."""

    # Create mock DataFrame using the shared helper
    schema = FinancialConglomeratePortfolioLegalPersonEconomicActivitySchema()
    mock_df = mock_dataframe_from_csv(
        mock_financial_conglomerates_portfolio_legal_person_economic_activity_csv_data, schema
    )
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
