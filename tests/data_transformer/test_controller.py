"""Testes do contrato aplicado pelo TransformerController.

Args:
    None.

Returns:
    None.

Raises:
    None.
"""

from pathlib import Path

import duckdb
import pytest
from pandas import DataFrame

from bacen_ifdata.data_loader.storage import DatabaseService
from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.data_transformer.schemas import (
    FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA,
)
from bacen_ifdata.data_transformer.schemas.base_schema import BaseSchema
from bacen_ifdata.data_transformer.transformer_factory import get_transformer
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


class RegionTestSchema(BaseSchema):
    """Esquema mínimo para testar a coluna calculada de região.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    SCHEMA_DEFINITION = {
        'uf': {'type': 'text'},
        'regiao': {'type': 'text'},
        'cidade': {'type': 'text'},
        'valor': {'type': 'text'},
    }


@pytest.fixture
def transformer_controller() -> TransformerController:
    """Cria o controlador com os transformadores do pacote.

    Args:
        None.

    Returns:
        O controlador de transformação.

    Raises:
        None.
    """
    return TransformerController(get_transformer)


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

    result = transformer_controller.transform(
        file_path=Path('dummy_path.csv'),
        schema=RegionTestSchema(),
        institution=Institutions.FINANCIAL_CONGLOMERATES,
    )

    assert isinstance(result, DataFrame)
    assert "regiao" in result.columns


@pytest.mark.parametrize(
    ('content', 'message'),
    [
        (
            'Instituição;Código\nBanco;101\n',
            'missing required column.*data_base',
        ),
        ('Instituição;Código;Data\nBanco;;03/2024\n', 'invalid value.*codigo'),
        ('Instituição;Código;Data\nBanco;101,5;03/2024\n', 'whole numbers'),
        (
            'Instituição;Código;Data\nBanco;101;13/2024\n',
            'invalid value.*data_base',
        ),
        (
            'Instituição;Código;Data\n ;101;03/2024\n',
            'invalid value.*instituicao',
        ),
    ],
)
def test_transform_rejects_invalid_identity(
    tmp_path: Path,
    transformer_controller: TransformerController,
    content: str,
    message: str,
) -> None:
    """Verifica os erros de cabeçalho e valor nos campos obrigatórios.

    Args:
        tmp_path: Diretório de teste.
        transformer_controller: Controlador com as regras de produção.
        content: Conteúdo do CSV inválido.
        message: Trecho esperado na mensagem de erro.

    Returns:
        None.

    Raises:
        None.
    """
    source = tmp_path / '2024-03.csv'
    source.write_text(content, encoding='utf-8')

    with pytest.raises(ValueError, match=f'2024-03.csv.*{message}'):
        transformer_controller.transform(
            source,
            FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA,
            Institutions.FINANCIAL_CONGLOMERATES,
        )


def test_transform_and_load_preserve_fraction_and_integer(
    tmp_path: Path, transformer_controller: TransformerController
) -> None:
    """Compara os tipos e valores após transformação e carga na Silver.

    Args:
        tmp_path: Diretório de teste.
        transformer_controller: Controlador com as regras de produção.

    Returns:
        None.

    Raises:
        None.
    """
    schema = FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA
    source = tmp_path / '2024-03.csv'
    source.write_text(
        'Instituição;Código;Data;Ativo Total;Cidade;Número de Agências\n'
        'Banco;9.007.199.254.740.993;03/2024;1.234,56;São Paulo;2.000,00\n',
        encoding='utf-8',
    )
    transformed = transformer_controller.transform(
        source, schema, Institutions.FINANCIAL_CONGLOMERATES
    )
    csv_path = tmp_path / 'typed.csv'
    transformed.iloc[:, ::-1].to_csv(csv_path, index=False)

    with duckdb.connect() as connection:
        database = DatabaseService(connection=connection)
        database.create_table('resumo', schema)
        database.insert_data('resumo', csv_path, schema)
        row = connection.execute(
            'SELECT codigo, typeof(codigo), ativo_total, typeof(ativo_total), '
            'numero_de_agencias, typeof(numero_de_agencias), '
            'cidade, regiao, lucro_liquido FROM resumo'
        ).fetchone()

    assert row == (
        9_007_199_254_740_993, 'BIGINT', pytest.approx(1_234.56), 'DOUBLE',
        2_000, 'BIGINT', 'São Paulo', None, None,
    )


def test_loader_rejects_missing_required_column(tmp_path: Path) -> None:
    """Impede a carga direta de um CSV tipado sem a data-base.

    Args:
        tmp_path: Diretório de teste.

    Returns:
        None.

    Raises:
        None.
    """
    schema = FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA
    csv_path = tmp_path / 'typed.csv'
    csv_path.write_text('instituicao,codigo\nBanco,101\n', encoding='utf-8')
    with duckdb.connect() as connection:
        database = DatabaseService(connection=connection)
        database.create_table('resumo', schema)
        with pytest.raises(
            ValueError, match='missing required column.*data_base'
        ):
            database.insert_data('resumo', csv_path, schema)
        row_count = connection.execute('SELECT count(*) FROM resumo')
        assert row_count.fetchone() == (0,)


def test_loader_rejects_fractional_integer(tmp_path: Path) -> None:
    """Garante que a carga rejeite códigos fracionários de forma atômica.

    Args:
        tmp_path: Diretório de teste.

    Returns:
        None.

    Raises:
        None.
    """
    schema = FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA
    csv_path = tmp_path / 'typed.csv'
    csv_path.write_text(
        'instituicao,codigo,data_base\n'
        'Banco A,101,2024-03-01\n'
        'Banco B,102.5,2024-03-01\n',
        encoding='utf-8',
    )
    with duckdb.connect() as connection:
        database = DatabaseService(connection=connection)
        database.create_table('resumo', schema)
        with pytest.raises(
            duckdb.Error, match='Expected an integer in codigo'
        ):
            database.insert_data('resumo', csv_path, schema)
        row_count = connection.execute('SELECT count(*) FROM resumo')
        assert row_count.fetchone() == (0,)
