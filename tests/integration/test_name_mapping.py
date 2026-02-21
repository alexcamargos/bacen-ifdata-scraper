"""Tests for the name mapping logic in the TransformerController."""

import pandas as pd

from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.data_transformer.schemas.interfaces import SchemaProtocol
from bacen_ifdata.utilities.string_utils import slugify


class MockSchema(SchemaProtocol):
    """A mock schema implementation for testing purposes."""

    def __init__(self, columns: list[str]):
        self.input_column_names = columns

    def get_type(self, column_name: str):
        return None


def test_slugify():
    """Test slugify function with various inputs."""

    assert slugify("Patrimônio Líquido") == "patrimonio_liquido"
    assert slugify("Ativo Total") == "ativo_total"
    assert slugify("  Disponibilidades (a)  ") == "disponibilidades_a"
    assert slugify("Patrimônio Líquido (i)") == "patrimonio_liquido_i"
    assert slugify("Lucro/Prejuízo") == "lucro_prejuizo"


def test_name_mapping_exact_match(mocker):
    """Test that exact matches are correctly mapped without relying on slugification."""

    # Setup
    mock_factory = mocker.Mock()
    controller = TransformerController(mock_factory)

    # Schema expects: ['ativo_total', 'patrimonio_liquido']
    schema = MockSchema(['ativo_total', 'patrimonio_liquido'])

    # CSV has: ['Ativo Total', 'Patrimônio Líquido']
    df = pd.DataFrame(columns=['Ativo Total', 'Patrimônio Líquido'])

    # Action
    mapping = controller._build_column_rename_map(df, schema)

    # Assert
    assert mapping['Ativo Total'] == 'ativo_total'
    assert mapping['Patrimônio Líquido'] == 'patrimonio_liquido'


def test_name_mapping_with_extra_columns_in_csv(mocker):
    """Test that extra columns in the CSV that are not in the schema
    are ignored and do not cause incorrect mappings.
    """

    mock_factory = mocker.Mock()
    controller = TransformerController(mock_factory)

    # Schema expects: ['ativo_total']
    schema = MockSchema(['ativo_total'])

    # CSV has: ['Ativo Total', 'Coluna Fantasma']
    df = pd.DataFrame(columns=['Ativo Total', 'Coluna Fantasma'])

    mapping = controller._build_column_rename_map(df, schema)

    # Should map 'Ativo Total'. Should IGNORE 'Coluna Fantasma'
    assert mapping['Ativo Total'] == 'ativo_total'
    assert 'Coluna Fantasma' not in mapping


def test_name_mapping_with_missing_columns_in_csv(mocker):
    """Test that if a column expected by the schema is missing in the CSV,
    it is not included in the mapping, and no incorrect mappings occur.
    """

    mock_factory = mocker.Mock()
    controller = TransformerController(mock_factory)

    # Schema expects: ['ativo_total', 'patrimonio_liquido']
    schema = MockSchema(['ativo_total', 'patrimonio_liquido'])

    # CSV has ONLY: ['Ativo Total'] (Patrimonio vanished)
    df = pd.DataFrame(columns=['Ativo Total'])

    mapping = controller._build_column_rename_map(df, schema)

    assert mapping['Ativo Total'] == 'ativo_total'
    # 'patrimonio_liquido' is not in mapping because source col doesn't exist
    # This ensures we don't map a wrong column to it.
    assert len(mapping) == 1
