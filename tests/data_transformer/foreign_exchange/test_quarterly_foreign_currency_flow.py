"""Tests for Foreign Exchange Quarterly Foreign Currency Flow data transformation schema."""

from pathlib import Path

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.data_transformer.schemas.foreign_exchange.quarterly_foreign_currency_flow import (
    ForeignExchangeQuarterlyForeignCurrencyFlowSchema,
)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


def test_foreign_exchange_quarterly_foreign_currency_flow_schema_structure():
    """Deve ter os nomes das colunas e tipos corretos definidos."""
    schema = ForeignExchangeQuarterlyForeignCurrencyFlowSchema()

    expected_structure = {
        'instituicao': TransformationType.TEXT,
        'codigo': TransformationType.NUMERIC,
        'consolidado_bancario': TransformationType.CATEGORICAL,
        'tipo_de_consolidacao': TransformationType.CATEGORICAL,
        'tipo_de_controle': TransformationType.CATEGORICAL,
        'segmento_resolucao': TransformationType.CATEGORICAL,
        'cidade': TransformationType.TEXT,
        'uf': TransformationType.CATEGORICAL,
        'regiao': TransformationType.CATEGORICAL,
        'data_base': TransformationType.DATE,
        'operacoes_comerciais_compra_numero_operacoes': TransformationType.NUMERIC,
        'operacoes_comerciais_compra_valor': TransformationType.NUMERIC,
        'operacoes_comerciais_venda_numero_operacoes': TransformationType.NUMERIC,
        'operacoes_comerciais_venda_valor': TransformationType.NUMERIC,
        'operacoes_comerciais_total_numero_operacoes': TransformationType.NUMERIC,
        'operacoes_comerciais_total_valor': TransformationType.NUMERIC,
        'operacoes_financeiras_compra_numero_operacoes': TransformationType.NUMERIC,
        'operacoes_financeiras_compra_valor': TransformationType.NUMERIC,
        'operacoes_financeiras_venda_numero_operacoes': TransformationType.NUMERIC,
        'operacoes_financeiras_venda_valor': TransformationType.NUMERIC,
        'operacoes_financeiras_total_numero_operacoes': TransformationType.NUMERIC,
        'operacoes_financeiras_total_valor': TransformationType.NUMERIC,
        'mercado_primario_total_numero_operacoes': TransformationType.NUMERIC,
        'mercado_primario_total_valor': TransformationType.NUMERIC,
        'mercado_interbancario_compra_numero_operacoes': TransformationType.NUMERIC,
        'mercado_interbancario_compra_valor': TransformationType.NUMERIC,
        'mercado_interbancario_venda_numero_operacoes': TransformationType.NUMERIC,
        'mercado_interbancario_venda_valor': TransformationType.NUMERIC,
        'mercado_interbancario_total_numero_operacoes': TransformationType.NUMERIC,
        'mercado_interbancario_total_valor': TransformationType.NUMERIC,
        'total_geral_numero_operacoes': TransformationType.NUMERIC,
        'total_geral_valor': TransformationType.NUMERIC,
    }

    assert set(schema.column_names) == set(expected_structure.keys())

    for column, expected_type in expected_structure.items():
        assert schema.get_type(column) == expected_type


def test_foreign_exchange_quarterly_foreign_currency_flow_transform_integration(
    mocker, mock_foreign_exchange_csv_data, transformer_factory, mock_dataframe_from_csv
):
    """Should transform Foreign Exchange Quarterly Foreign Currency Flow data correctly."""

    # Create mock DataFrame using the shared helper
    schema = ForeignExchangeQuarterlyForeignCurrencyFlowSchema()
    mock_df = mock_dataframe_from_csv(mock_foreign_exchange_csv_data, schema)
    mocker.patch('bacen_ifdata.data_transformer.controller.load_csv_data', return_value=mock_df)

    # Use the shared transformer factory fixture
    controller = TransformerController(transformer_factory)

    result = controller.transform(file_path=Path("dummy.csv"), schema=schema, institution=Institutions.FOREIGN_EXCHANGE)

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
