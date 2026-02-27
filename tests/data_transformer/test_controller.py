"""Testes unitários para a classe TransformerController."""

import pytest
from pandas import DataFrame

from bacen_ifdata.data_transformer.controller import TransformationType, TransformerController
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


class MockTransformer:
    """Mock para a classe Transformer."""

    def transform_numeric_columns(self, df: DataFrame, columns: list[str]) -> DataFrame:
        return df

    def transform_percentage_columns(self, df: DataFrame, columns: list[str]) -> DataFrame:
        return df

    def transform_date_columns(self, df: DataFrame, columns: list[str]) -> DataFrame:
        return df

    def transform_categorical_columns(self, df: DataFrame, columns: list[str]) -> DataFrame:
        return df

    def transform_text_columns(self, df: DataFrame, columns: list[str]) -> DataFrame:
        return df

    def apply_business_rules(self, df: DataFrame) -> DataFrame:
        return df

    def deduplicate_dataset(self, df: DataFrame, schema=None) -> DataFrame:
        return df


# pylint: disable=too-few-public-methods
class MockSchema:
    """Mock para a classe Schema."""

    column_names = ['uf', 'cidade', 'valor']

    def get_type(self, column_name: str) -> TransformationType:
        """Retorna o tipo de transformação para uma coluna específica."""

        return TransformationType.TEXT

    @property
    def input_column_names(self) -> list[str]:
        """Retorna os nomes das colunas de entrada (neste mock, igual a column_names)."""

        return self.column_names


@pytest.fixture
def transformer_controller():
    """Fixture que retorna uma instância de TransformerController com um mock factory."""

    def factory(institution):
        """Mock factory que retorna uma instância de MockTransformer para qualquer instituição."""

        return MockTransformer()

    return TransformerController(factory)


def test_get_transformer_caching(transformer_controller: TransformerController):
    """Deve armazenar em cache as instâncias do transformador."""

    t1 = transformer_controller._get_transformer(Institutions.FINANCIAL_CONGLOMERATES)
    t2 = transformer_controller._get_transformer(Institutions.FINANCIAL_CONGLOMERATES)

    assert t1 is t2


def test_create_region_column(transformer_controller: TransformerController):
    """Deve criar a coluna 'regiao' baseada no mapeamento de 'uf'."""

    data = {"uf": ["SP", "AC"], "cidade": ["Sao Paulo", "Rio Branco"]}
    df = DataFrame(data)

    # Testa o método privado responsável pela criação da região.
    result = transformer_controller._create_region_column(df)

    assert "regiao" in result.columns
    assert result.iloc[0]["regiao"] == "Sudeste"  # Knowing SP is Sudeste
    assert result.iloc[1]["regiao"] == "Norte"  # Knowing AC is Norte


def test_transform_pipeline(transformer_controller: TransformerController, mocker):
    """Deve executar o pipeline de transformação completo."""

    # Mock do método de carregamento de dados para evitar I/O
    mocker.patch.object(
        transformer_controller,
        "_load_data",
        return_value=DataFrame({"uf": ["SP"], "cidade": ["Sao Paulo"], "valor": ["10"]}),
    )

    mock_schema = MockSchema()

    result = transformer_controller.transform(
        file_path="dummy_path.csv", schema=mock_schema, institution=Institutions.FINANCIAL_CONGLOMERATES
    )

    assert isinstance(result, DataFrame)
    assert "regiao" in result.columns
