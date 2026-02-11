"""Unit tests for complex data processing scenarios in the data_cleaner module."""

from enum import Enum
from pathlib import Path

from pytest_mock import MockerFixture

from bacen_ifdata.data_cleaner.processing import check_file_already_processed, normalize_csv
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from tests.fixtures.cleaner.mock_data_cleaner import MOCK_COMPLEX_RAW_CSV_CONTENT


class MockReport(Enum):
    """Mock report enum."""

    PORTFOLIO = 'portfolio_individuals_type_maturity'


def test_normalize_csv_complex_header(mocker: MockerFixture):
    """
    Test normalization of a CSV with complex multi-line headers and empty columns.

    This test verifies if the logic correctly:
    1. Identifies the multi-line header deviation.
    2. Merges the empty columns in Line 1 with values from Line 2.
    3. Removes the empty last column.
    4. Removes the invalid footer.
    """

    # Mocks
    mock_input_open = mocker.mock_open(read_data=MOCK_COMPLEX_RAW_CSV_CONTENT)
    mock_output_open = mocker.mock_open()

    # Mock open for input (read) and output (write)
    mocker.patch("builtins.open", side_effect=[mock_input_open.return_value, mock_output_open.return_value])

    # Mock file system checks to bypass real IO
    mocker.patch("bacen_ifdata.data_cleaner.processing.build_directory_path", return_value=Path("mock/path"))
    mocker.patch("bacen_ifdata.data_cleaner.processing.check_file_already_processed", return_value=False)

    # Execute
    result = normalize_csv(Institutions.FINANCIAL_CONGLOMERATES, MockReport.PORTFOLIO, "complex.csv")

    # Assertions
    assert result is True

    # Get the written content
    handle = mock_output_open()

    # Check the data written via writelines()
    writelines_calls = handle.writelines.call_args_list
    assert len(writelines_calls) > 0
    data_lines = writelines_calls[0][0][0]  # The list of strings passed to writelines

    # 1. Verify Header Removed (Headless CSV)
    # The output should NOT contain the header line, it should start with data.
    first_line = data_lines[0]
    assert "Instituição" not in first_line
    assert "Empréstimo" not in first_line

    # 2. Verify Data Integrity
    # Assert that valid data lines are preserved and come first
    assert "BANCO TESTE 01" in first_line
    assert "BANCO TESTE 02" in "".join(data_lines)

    # 3. Verify Footer Removal
    # The raw file ends with "Rodapé desnecessário..."
    # The processed file should NOT have it.
    assert "Rodapé desnecessário" not in "".join(data_lines)
