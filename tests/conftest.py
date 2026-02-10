import sys
from io import StringIO
from pathlib import Path

# Add tests directory to sys.path
tests_dir = Path(__file__).parent
if str(tests_dir) not in sys.path:
    sys.path.insert(0, str(tests_dir))


import pandas as pd
import polars as pl
import pytest

from .fixtures.mock_data import (
    MOCK_COMPLEX_CSV_CONTENT_PROCESSED,
    MOCK_COMPLEX_RAW_CSV_CONTENT,
    MOCK_FINANCIAL_CONGLOMERATES_ASSETS_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_INCOME_STATEMENT_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_LIABILITIES_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_GEOGRAPHIC_REGION_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_INDEXER_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_INDIVIDUALS_TYPE_MATURITY_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_NUMBER_CLIENTS_OPERATIONS_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_RISK_LEVEL_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_GEOGRAPHIC_REGION_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_INDEXER_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_INDIVIDUALS_TYPE_MATURITY_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_NUMBER_CLIENTS_OPERATIONS_CSV,
    MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_RISK_LEVEL_CSV,
    MOCK_FOREIGN_EXCHANGE_CSV,
    MOCK_INDIVIDUAL_INSTITUTIONS_ASSETS_CSV,
    MOCK_INDIVIDUAL_INSTITUTIONS_CSV,
    MOCK_INDIVIDUAL_INSTITUTIONS_INCOME_STATEMENT_CSV,
    MOCK_INDIVIDUAL_INSTITUTIONS_LIABILITIES_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_ASSETS_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_CAPITAL_INFORMATION_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_INCOME_STATEMENT_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_LIABILITIES_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_GEOGRAPHIC_REGION_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_INDEXER_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_INDIVIDUALS_TYPE_MATURITY_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_NUMBER_CLIENTS_OPERATIONS_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_RISK_LEVEL_CSV,
    MOCK_PRUDENTIAL_CONGLOMERATE_SEGMENTATION_CSV,
    MOCK_SIMPLE_RAW_CSV_CONTENT,
    MOCK_SIMPLE_RAW_CSV_CONTENT_PROCESSED,
    MOCK_TRANSFORMER_INPUT_CSV,
)


@pytest.fixture
def mock_transformers_data_schema():
    """Returns a schema dict for the mock data."""

    return {
        "Instituição": pl.Utf8,
        "Código": pl.Utf8,
        "TCB": pl.Utf8,
        "SR": pl.Utf8,
        "TD": pl.Utf8,
        "TC": pl.Utf8,
        "Cidade": pl.Utf8,
        "UF": pl.Utf8,
        "Data": pl.Utf8,
        "Ativo Total": pl.Utf8,  # Kept as string to simulate initial CSV load
        "Carteira de Crédito Classificada": pl.Utf8,
    }


@pytest.fixture
def mock_polars_df(mock_transformers_data_schema):
    """Returns a Polars DataFrame created from the mock CSV data."""

    return pl.read_csv(StringIO(MOCK_TRANSFORMER_INPUT_CSV), separator=";", dtypes=mock_transformers_data_schema)


@pytest.fixture
def mock_pandas_df():
    """Returns a Pandas DataFrame created from the mock CSV data, simulating the current scraper behavior."""

    return pd.read_csv(StringIO(MOCK_TRANSFORMER_INPUT_CSV), sep=";", dtype=str)


@pytest.fixture
def transformer_factory():
    """Returns a factory function that creates BaseTransformer instances.

    This fixture uses the Factory Pattern to enable dynamic object creation
    within tests, allowing arguments (like 'institution') to be passed, which
    standard fixtures do not support directly.

    The import is performed locally to avoid circular dependencies and ensure
    lazy loading, optimizing test collection performance.
    """

    # Import the BaseTransformer class here to avoid circular imports when defining the factory function.
    # pylint: disable=import-outside-toplevel
    from bacen_ifdata.data_transformer.transformers.base import BaseTransformer

    def factory(institution):  # pylint: disable=unused-argument
        """Factory function that returns a BaseTransformer instance.

        Args:
            institution: The institution type (unused in base transformer)

        Returns:
            BaseTransformer: A new transformer instance
        """

        return BaseTransformer()

    return factory


@pytest.fixture
def mock_dataframe_from_csv():
    """Returns a helper function to create mock DataFrames from CSV strings.

    This fixture provides a reusable helper for creating properly formatted
    DataFrames that match the schema's column naming conventions.

    Returns:
        Callable: A function that takes (csv_string, schema) and returns a DataFrame
    """

    def create_mock_df(csv_string: str, schema):
        """Create a mock DataFrame from CSV string using schema column names.

        Args:
            csv_string: The CSV data as a string
            schema: The schema object with column_names property

        Returns:
            pd.DataFrame: A DataFrame with schema-compliant column names
        """

        return pd.read_csv(StringIO(csv_string), sep=';', names=schema.column_names, dtype=str, skiprows=1, header=0)

    return create_mock_df


# Financial Conglomerates CSV Data Fixtures


@pytest.fixture
def mock_financial_conglomerates_csv_data():
    """Mock CSV data for Financial Conglomerates Summary."""

    return MOCK_FINANCIAL_CONGLOMERATES_CSV


@pytest.fixture
def mock_financial_conglomerates_assets_csv_data():
    """Mock CSV data for Financial Conglomerates Assets."""

    return MOCK_FINANCIAL_CONGLOMERATES_ASSETS_CSV


@pytest.fixture
def mock_financial_conglomerates_liabilities_csv_data():
    """Mock CSV data for Financial Conglomerates Liabilities."""

    return MOCK_FINANCIAL_CONGLOMERATES_LIABILITIES_CSV


@pytest.fixture
def mock_financial_conglomerates_income_statement_csv_data():
    """Mock CSV data for Financial Conglomerates Income Statement."""

    return MOCK_FINANCIAL_CONGLOMERATES_INCOME_STATEMENT_CSV


@pytest.fixture
def mock_financial_conglomerates_portfolio_geographic_region_csv_data():
    """Mock CSV data for Financial Conglomerates Portfolio Geographic Region."""

    return MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_GEOGRAPHIC_REGION_CSV


@pytest.fixture
def mock_financial_conglomerates_portfolio_indexer_csv_data():
    """Mock CSV data for Financial Conglomerates Portfolio Indexer."""

    return MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_INDEXER_CSV


@pytest.fixture
def mock_financial_conglomerates_portfolio_risk_level_csv_data():
    """Mock CSV data for Financial Conglomerates Portfolio Risk Level."""

    return MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_RISK_LEVEL_CSV


@pytest.fixture
def mock_financial_conglomerates_portfolio_number_clients_operations_csv_data():
    """Mock CSV data for Financial Conglomerates Portfolio Number of Clients and Operations."""

    return MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_NUMBER_CLIENTS_OPERATIONS_CSV


@pytest.fixture
def mock_financial_conglomerates_portfolio_individuals_type_maturity_csv_data():
    """Mock CSV data for Financial Conglomerates Portfolio Individuals Type/Maturity."""

    return MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_INDIVIDUALS_TYPE_MATURITY_CSV


@pytest.fixture
def mock_financial_conglomerates_portfolio_legal_person_business_size_csv_data():
    """Mock CSV data for Financial Conglomerates Portfolio Legal Person Business Size."""

    return MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE_CSV


@pytest.fixture
def mock_financial_conglomerates_portfolio_legal_person_economic_activity_csv_data():
    """Mock CSV data for Financial Conglomerates Portfolio Legal Person Economic Activity."""

    return MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY_CSV


@pytest.fixture
def mock_financial_conglomerates_portfolio_legal_person_type_maturity_csv_data():
    """Mock CSV data for Financial Conglomerates Portfolio Legal Person Type/Maturity."""

    return MOCK_FINANCIAL_CONGLOMERATES_PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY_CSV


# Prudential Conglomerates CSV Data Fixtures


@pytest.fixture
def mock_prudential_conglomerate_csv_data():
    """Mock CSV data for Prudential Conglomerate Summary."""
    return MOCK_PRUDENTIAL_CONGLOMERATE_CSV


@pytest.fixture
def mock_prudential_conglomerate_assets_csv_data():
    """Mock CSV data for Prudential Conglomerate Assets."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_ASSETS_CSV


@pytest.fixture
def mock_prudential_conglomerate_liabilities_csv_data():
    """Mock CSV data for Prudential Conglomerate Liabilities."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_LIABILITIES_CSV


@pytest.fixture
def mock_prudential_conglomerate_income_statement_csv_data():
    """Mock CSV data for Prudential Conglomerate Income Statement."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_INCOME_STATEMENT_CSV


@pytest.fixture
def mock_prudential_conglomerate_capital_information_csv_data():
    """Mock CSV data for Prudential Conglomerate Capital Information."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_CAPITAL_INFORMATION_CSV


@pytest.fixture
def mock_prudential_conglomerate_segmentation_csv_data():
    """Mock CSV data for Prudential Conglomerate Segmentation."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_SEGMENTATION_CSV


@pytest.fixture
def mock_prudential_conglomerate_portfolio_geographic_region_csv_data():
    """Mock CSV data for Prudential Conglomerate Portfolio Geographic Region."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_GEOGRAPHIC_REGION_CSV


@pytest.fixture
def mock_prudential_conglomerate_portfolio_indexer_csv_data():
    """Mock CSV data for Prudential Conglomerate Portfolio Indexer."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_INDEXER_CSV


@pytest.fixture
def mock_prudential_conglomerate_portfolio_individuals_type_maturity_csv_data():
    """Mock CSV data for Prudential Conglomerate Portfolio Individuals Type Maturity."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_INDIVIDUALS_TYPE_MATURITY_CSV


@pytest.fixture
def mock_prudential_conglomerate_portfolio_legal_person_business_size_csv_data():
    """Mock CSV data for Prudential Conglomerate Portfolio Legal Person Business Size."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE_CSV


@pytest.fixture
def mock_prudential_conglomerate_portfolio_legal_person_economic_activity_csv_data():
    """Mock CSV data for Prudential Conglomerate Portfolio Legal Person Economic Activity."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY_CSV


@pytest.fixture
def mock_prudential_conglomerate_portfolio_legal_person_type_maturity_csv_data():
    """Mock CSV data for Prudential Conglomerate Portfolio Legal Person Type Maturity."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY_CSV


@pytest.fixture
def mock_prudential_conglomerate_portfolio_number_clients_operations_csv_data():
    """Mock CSV data for Prudential Conglomerate Portfolio Number of Clients and Operations."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_NUMBER_CLIENTS_OPERATIONS_CSV


@pytest.fixture
def mock_prudential_conglomerate_portfolio_risk_level_csv_data():
    """Mock CSV data for Prudential Conglomerate Portfolio Risk Level."""

    return MOCK_PRUDENTIAL_CONGLOMERATE_PORTFOLIO_RISK_LEVEL_CSV


# Individual Institutions CSV Data Fixtures


@pytest.fixture
def mock_individual_institutions_csv_data():
    """Mock CSV data for Individual Institutions Summary."""

    return MOCK_INDIVIDUAL_INSTITUTIONS_CSV


@pytest.fixture
def mock_individual_institutions_assets_csv_data():
    """Mock CSV data for Individual Institutions Assets."""

    return MOCK_INDIVIDUAL_INSTITUTIONS_ASSETS_CSV


@pytest.fixture
def mock_individual_institutions_liabilities_csv_data():
    """Mock CSV data for Individual Institutions Liabilities."""

    return MOCK_INDIVIDUAL_INSTITUTIONS_LIABILITIES_CSV


@pytest.fixture
def mock_individual_institutions_income_statement_csv_data():
    """Mock CSV data for Individual Institutions Income Statement."""

    return MOCK_INDIVIDUAL_INSTITUTIONS_INCOME_STATEMENT_CSV


# Financial Conglomerates SCR CSV Data Fixtures


@pytest.fixture
def mock_financial_conglomerates_scr_portfolio_csv_data():
    """Mock CSV data for Financial Conglomerates SCR Portfolio."""

    return MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_CSV


@pytest.fixture
def mock_financial_conglomerates_scr_portfolio_geographic_region_csv_data():
    """Mock CSV data for Financial Conglomerates SCR Portfolio Geographic Region."""

    return MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_GEOGRAPHIC_REGION_CSV


@pytest.fixture
def mock_financial_conglomerates_scr_portfolio_legal_person_economic_activity_csv_data():
    """Mock CSV data for Financial Conglomerates SCR Portfolio Legal Person Economic Activity."""

    return MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY_CSV


@pytest.fixture
def mock_financial_conglomerates_scr_portfolio_individuals_type_maturity_csv_data():
    """Mock CSV data for Financial Conglomerates SCR Portfolio Individuals Type Maturity."""

    return MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_INDIVIDUALS_TYPE_MATURITY_CSV


@pytest.fixture
def mock_financial_conglomerates_scr_portfolio_legal_person_type_maturity_csv_data():
    """Mock CSV data for Financial Conglomerates SCR Portfolio Legal Person Type/Maturity."""

    return MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY_CSV


@pytest.fixture
def mock_financial_conglomerates_scr_portfolio_legal_person_business_size_csv_data():
    """Mock CSV data for Financial Conglomerates SCR Portfolio Legal Person Business Size."""

    return MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE_CSV


@pytest.fixture
def mock_financial_conglomerates_scr_portfolio_indexer_csv_data():
    """Mock CSV data for Financial Conglomerates SCR Portfolio Indexer."""

    return MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_INDEXER_CSV


@pytest.fixture
def mock_financial_conglomerates_scr_portfolio_risk_level_csv_data():
    """Mock CSV data for Financial Conglomerates SCR Portfolio Risk Level."""

    return MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_RISK_LEVEL_CSV


@pytest.fixture
def mock_financial_conglomerates_scr_portfolio_number_clients_operations_csv_data():
    """Mock CSV data for Financial Conglomerates SCR Portfolio Number of Clients and Operations."""

    return MOCK_FINANCIAL_CONGLOMERATES_SCR_PORTFOLIO_NUMBER_CLIENTS_OPERATIONS_CSV


# Foreign Exchange CSV Data Fixture


@pytest.fixture
def mock_foreign_exchange_csv_data():
    """Mock CSV data for Foreign Exchange Quarterly Foreign Currency Flow."""

    return MOCK_FOREIGN_EXCHANGE_CSV
