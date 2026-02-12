"""Tests for Individual Institutions Liabilities data transformation schema."""

from pathlib import Path

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.data_transformer.schemas.individual_institutions.liabilities import (
    IndividualInstitutionLiabilitiesSchema,
)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


def test_individual_institutions_liabilities_schema_structure():
    """Deve ter os nomes das colunas e tipos corretos definidos."""
    schema = IndividualInstitutionLiabilitiesSchema()

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
        'regiao': TransformationType.CATEGORICAL,
        'data_base': TransformationType.DATE,
        'depositos_vista': TransformationType.NUMERIC,
        'depositos_poupanca': TransformationType.NUMERIC,
        'depositos_interfinanceiros': TransformationType.NUMERIC,
        'depositos_a_prazo': TransformationType.NUMERIC,
        'conta_de_pagamento_pre_paga': TransformationType.NUMERIC,
        'depositos_outros': TransformationType.NUMERIC,
        'deposito_total': TransformationType.NUMERIC,
        'obrigacoes_operacoes_compromissadas': TransformationType.NUMERIC,
        'letras_de_credito_imobiliario': TransformationType.NUMERIC,
        'letras_de_credito_agronegocio': TransformationType.NUMERIC,
        'letras_financeiras': TransformationType.NUMERIC,
        'obrigacoes_titulos_e_valores_mobiliarios_exterior': TransformationType.NUMERIC,
        'outros_recursos_de_aceites_e_emissao_de_titulos': TransformationType.NUMERIC,
        'recursos_de_aceites_e_emissao_de_titulos': TransformationType.NUMERIC,
        'obrigacoes_emprestimos_e_repasses': TransformationType.NUMERIC,
        'captacoes': TransformationType.NUMERIC,
        'instrumentos_derivativos': TransformationType.NUMERIC,
        'outras_obrigacoes': TransformationType.NUMERIC,
        'passivo_circulante_exigivel_a_longo_prazo': TransformationType.NUMERIC,
        'patrimonio_liquido': TransformationType.NUMERIC,
        'passivo_total': TransformationType.NUMERIC,
    }

    assert set(schema.column_names) == set(expected_structure.keys())

    for column, expected_type in expected_structure.items():
        assert schema.get_type(column) == expected_type


def test_individual_institutions_liabilities_transform_integration(
    mocker, mock_individual_institutions_liabilities_csv_data, transformer_factory, mock_dataframe_from_csv
):
    """Should transform Individual Institutions Liabilities data correctly."""

    # Create mock DataFrame using the shared helper
    schema = IndividualInstitutionLiabilitiesSchema()
    mock_df = mock_dataframe_from_csv(mock_individual_institutions_liabilities_csv_data, schema)
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
