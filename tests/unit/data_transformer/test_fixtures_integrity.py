"""Tests for data fixture integrity."""

from io import StringIO

import pandas as pd
import pytest

from bacen_ifdata.data_transformer.schemas.financial_conglomerates.assets import FinancialConglomeratesAssetsSchema
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.income_statement import (
    FinancialConglomerateIncomeStatementSchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.liabilities import (
    FinancialConglomerateLiabilitiesSchema,
)


def test_financial_conglomerates_assets_mock_integrity(
    mock_financial_conglomerates_assets_csv_data,
):
    """Ensure mock CSV for Financial Conglomerates Assets matches the Schema structure."""
    schema = FinancialConglomeratesAssetsSchema()

    # Read CSV without forcing names, to check the actual headers in the mock string
    df = pd.read_csv(StringIO(mock_financial_conglomerates_assets_csv_data), sep=';')
    csv_columns = [col.strip() for col in df.columns]

    # Verify column count matches (System relies on positional mapping)
    assert len(csv_columns) == len(schema.input_column_names), (
        f"Column count mismatch!\n"
        f"CSV has {len(csv_columns)} columns: {csv_columns}\n"
        f"Schema expects {len(schema.input_column_names)}: {schema.input_column_names}"
    )


def test_financial_conglomerates_liabilities_mock_integrity(
    mock_financial_conglomerates_liabilities_csv_data,
):
    """Ensure mock CSV for Financial Conglomerates Liabilities matches the Schema structure."""
    schema = FinancialConglomerateLiabilitiesSchema()

    df = pd.read_csv(StringIO(mock_financial_conglomerates_liabilities_csv_data), sep=';')
    csv_columns = [col.strip() for col in df.columns]

    assert len(csv_columns) == len(schema.input_column_names), (
        f"Column count mismatch!\n"
        f"CSV has {len(csv_columns)} columns\n"
        f"Schema expects {len(schema.input_column_names)}"
    )


def test_financial_conglomerates_income_statement_mock_integrity(
    mock_financial_conglomerates_income_statement_csv_data,
):
    """Ensure mock CSV for Financial Conglomerates Income Statement matches the Schema structure."""
    schema = FinancialConglomerateIncomeStatementSchema()

    df = pd.read_csv(StringIO(mock_financial_conglomerates_income_statement_csv_data), sep=';')
    csv_columns = [col.strip() for col in df.columns]

    assert len(csv_columns) == len(schema.input_column_names), (
        f"Column count mismatch!\n"
        f"CSV has {len(csv_columns)} columns\n"
        f"Schema expects {len(schema.input_column_names)}"
    )
