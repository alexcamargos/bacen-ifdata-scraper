"""Tests for Prudential Conglomerates Portfolio Legal Person Business Size data transformation schema."""

from pathlib import Path

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.portfolio_legal_person_type_maturity import (
    PrudentialConglomeratePortfolioLegalPersonTypeMaturitySchema,
)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


def test_prudential_conglomerates_portfolio_legal_person_type_maturity_schema_structure():
    """Test that the Prudential Conglomerates Portfolio Legal Person Type Maturity schema has
    correct column names and transformation types.
    """

    schema = PrudentialConglomeratePortfolioLegalPersonTypeMaturitySchema()

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
        'capital_giro_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'capital_giro_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'capital_giro_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'capital_giro_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'capital_giro_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'capital_giro_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'capital_giro_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'capital_giro_total': TransformationType.NUMERIC,
        'investimento_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'investimento_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'investimento_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'investimento_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'investimento_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'investimento_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'investimento_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'investimento_total': TransformationType.NUMERIC,
        'cheque_especial_conta_garantida_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'cheque_especial_conta_garantida_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'cheque_especial_conta_garantida_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'cheque_especial_conta_garantida_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'cheque_especial_conta_garantida_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'cheque_especial_conta_garantida_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'cheque_especial_conta_garantida_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'cheque_especial_conta_garantida_total': TransformationType.NUMERIC,
        'operacoes_recebiveis_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'operacoes_recebiveis_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'operacoes_recebiveis_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'operacoes_recebiveis_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'operacoes_recebiveis_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'operacoes_recebiveis_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'operacoes_recebiveis_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'operacoes_recebiveis_total': TransformationType.NUMERIC,
        'comercio_exterior_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'comercio_exterior_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'comercio_exterior_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'comercio_exterior_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'comercio_exterior_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'comercio_exterior_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'comercio_exterior_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'comercio_exterior_total': TransformationType.NUMERIC,
        'outros_creditos_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'outros_creditos_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'outros_creditos_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'outros_creditos_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'outros_creditos_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'outros_creditos_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'outros_creditos_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'outros_creditos_total': TransformationType.NUMERIC,
        'financiamento_infraestrutura_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'financiamento_infraestrutura_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'financiamento_infraestrutura_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'financiamento_infraestrutura_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'financiamento_infraestrutura_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'financiamento_infraestrutura_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'financiamento_infraestrutura_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'financiamento_infraestrutura_total': TransformationType.NUMERIC,
        'rural_agroindustrial_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'rural_agroindustrial_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'rural_agroindustrial_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'rural_agroindustrial_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'rural_agroindustrial_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'rural_agroindustrial_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'rural_agroindustrial_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'rural_agroindustrial_total': TransformationType.NUMERIC,
        'habitacional_vencido_a_partir_15_dias': TransformationType.NUMERIC,
        'habitacional_a_vencer_ate_90_dias': TransformationType.NUMERIC,
        'habitacional_a_vencer_91_a_360_dias': TransformationType.NUMERIC,
        'habitacional_a_vencer_361_a_1080_dias': TransformationType.NUMERIC,
        'habitacional_a_vencer_1081_a_1800_dias': TransformationType.NUMERIC,
        'habitacional_a_vencer_1801_a_5400_dias': TransformationType.NUMERIC,
        'habitacional_a_vencer_acima_5400_dias': TransformationType.NUMERIC,
        'habitacional_total': TransformationType.NUMERIC,
        'total_exterior_pessoa_juridica': TransformationType.NUMERIC,
    }

    assert set(schema.column_names) == set(expected_structure.keys())

    for column, expected_type in expected_structure.items():
        assert schema.get_type(column) == expected_type


def test_prudential_conglomerates_portfolio_legal_person_type_maturity_transform_integration(
    mocker,
    mock_prudential_conglomerate_portfolio_legal_person_type_maturity_csv_data,
    transformer_factory,
    mock_dataframe_from_csv,
):
    """Should transform Prudential Conglomerates Portfolio Legal Person Type Maturity data correctly."""

    # Create mock DataFrame using the shared helper
    schema = PrudentialConglomeratePortfolioLegalPersonTypeMaturitySchema()
    mock_df = mock_dataframe_from_csv(
        mock_prudential_conglomerate_portfolio_legal_person_type_maturity_csv_data, schema
    )
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
