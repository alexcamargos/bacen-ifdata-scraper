"""Testes unitários para as funções de processamento de dados do módulo data_cleaner."""

from enum import StrEnum
from pathlib import Path

from pytest_mock import MockerFixture

from bacen_ifdata.data_cleaner.processing import check_file_already_processed, normalize_csv
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from tests.fixtures.mock_data import MOCK_SIMPLE_RAW_CSV_CONTENT


class MockReport(StrEnum):
    """Enum de relatório simulado para testes."""

    SUMMARY = 'summary'


def test_check_file_already_processed_true(tmp_path: Path):
    """Deve retornar True se o arquivo existir no diretório de saída."""

    test_file = "test.csv"
    (tmp_path / test_file).touch()

    assert check_file_already_processed(tmp_path, test_file) is True


def test_check_file_already_processed_false(tmp_path: Path):
    """Deve retornar False se o arquivo não existir no diretório de saída."""

    test_file = "test.csv"

    assert check_file_already_processed(tmp_path, test_file) is False


def test_normalize_csv_success(mocker: MockerFixture):
    """Deve normalizar com sucesso um arquivo CSV bruto."""

    # Mocks
    mock_input_open = mocker.mock_open(read_data=MOCK_SIMPLE_RAW_CSV_CONTENT)
    mock_output_open = mocker.mock_open()

    # Precisamos lidar com múltiplas chamadas de open: uma para leitura (input), outra para escrita (output).
    # side_effect nos permite retornar diferentes file handles para chamadas consecutivas.
    mocker.patch("builtins.open", side_effect=[mock_input_open.return_value, mock_output_open.return_value])

    # Mock directory paths to avoid attempting real file system access
    mocker.patch("bacen_ifdata.data_cleaner.processing.build_directory_path", return_value=Path("mock/path"))
    mocker.patch("bacen_ifdata.data_cleaner.processing.check_file_already_processed", return_value=False)

    result = normalize_csv(Institutions.FINANCIAL_CONGLOMERATES, MockReport.SUMMARY, "test.csv")

    assert result is True

    # Verifica se a escrita foi chamada.
    # O header normalizado é escrito via write() e os dados via writelines().
    mock_output_open.return_value.write.assert_called()  # Header
    mock_output_open.return_value.writelines.assert_called()  # Data


def test_normalize_csv_already_processed(mocker: MockerFixture):
    """Deve pular o processamento se o arquivo já estiver normalizado."""

    mocker.patch("bacen_ifdata.data_cleaner.processing.build_directory_path", return_value=Path("mock/path"))
    mocker.patch("bacen_ifdata.data_cleaner.processing.check_file_already_processed", return_value=True)

    result = normalize_csv(Institutions.FINANCIAL_CONGLOMERATES, MockReport.SUMMARY, "test.csv")

    assert result is False


def test_normalize_csv_file_not_found(mocker: MockerFixture):
    """Deve lidar com FileNotFoundError graciosamente."""

    mocker.patch("bacen_ifdata.data_cleaner.processing.build_directory_path", return_value=Path("mock/path"))
    mocker.patch("bacen_ifdata.data_cleaner.processing.check_file_already_processed", return_value=False)
    mocker.patch("builtins.open", side_effect=FileNotFoundError)

    result = normalize_csv(Institutions.FINANCIAL_CONGLOMERATES, MockReport.SUMMARY, "test.csv")

    assert result is False
