import sys
from pathlib import Path
from typing import Any, Type

import pandas as pd
import pytest

from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.assets import FinancialConglomeratesAssetsSchema
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.capital_information import (
    FinancialConglomerateCapitalInformationSchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.income_statement import (
    FinancialConglomerateIncomeStatementSchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.liabilities import (
    FinancialConglomerateLiabilitiesSchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.summary import FinancialConglomerateSummarySchema
from bacen_ifdata.data_transformer.schemas.financial_conglomerates_scr.portfolio_individuals_type_maturity import (
    FinancialConglomerateSCRPortfolioIndividualsTypeMaturitySchema,
)
from bacen_ifdata.data_transformer.schemas.foreign_exchange.quarterly_foreign_currency_flow import (
    ForeignExchangeQuarterlyForeignCurrencyFlowSchema,
)
from bacen_ifdata.data_transformer.schemas.individual_institutions.assets import IndividualInstitutionAssetsSchema
from bacen_ifdata.data_transformer.schemas.individual_institutions.income_statement import (
    IndividualInstitutionIncomeStatementSchema,
)
from bacen_ifdata.data_transformer.schemas.individual_institutions.liabilities import (
    IndividualInstitutionLiabilitiesSchema,
)
from bacen_ifdata.data_transformer.schemas.individual_institutions.summary import IndividualInstitutionSummarySchema
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.assets import PrudentialConglomeratesAssetsSchema
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.capital_information import (
    PrudentialConglomerateCapitalInformationSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.income_statement import (
    PrudentialConglomerateIncomeStatementSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.liabilities import (
    PrudentialConglomerateLiabilitiesSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.segmentation import (
    PrudentialConglomerateSegmentationSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.summary import PrudentialConglomerateSummarySchema
from bacen_ifdata.data_transformer.transformers.base import BaseTransformer
from bacen_ifdata.scraper.institutions import InstitutionType
from bacen_ifdata.utilities.configurations import Config


@pytest.fixture
def controller():
    # Mock factory as we rely on the BaseTransformer's generic logic + Controller's orchestration

    return TransformerController(lambda inst: BaseTransformer())


def normalize_value(val: Any) -> str:
    """Normalizes a value for string comparison (removes dots, handles NaNs)."""

    if pd.isna(val) or str(val).lower() == "nan":
        return "nan"

    return str(val).strip().replace('.', '')


@pytest.mark.parametrize(
    "institution_type, schema_class, file_rel_path, key_fields",
    [
        # --- Prudential Conglomerates ---
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            PrudentialConglomerateLiabilitiesSchema,
            "data/processed/prudential_conglomerates/liabilities/2023-06.csv",
            [("instituicao", 0), ("data_base", 8), ("patrimonio_liquido", 29)],
        ),
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            PrudentialConglomeratesAssetsSchema,
            "data/processed/prudential_conglomerates/assets/2014-03.csv",
            [("instituicao", 0), ("data_base", 8)],
        ),
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            PrudentialConglomerateIncomeStatementSchema,
            "data/processed/prudential_conglomerates/income_statement/2014-03.csv",
            [("instituicao", 0), ("data_base", 8)],
        ),
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            PrudentialConglomerateCapitalInformationSchema,
            "data/processed/prudential_conglomerates/capital_information/2015-03.csv",
            [("instituicao", 0), ("data_base", 8)],
        ),
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            PrudentialConglomerateSegmentationSchema,
            "data/processed/prudential_conglomerates/segmentation/2017-03.csv",
            [("instituicao", 0), ("data_base", 7)],
        ),
        (
            InstitutionType.PRUDENTIAL_CONGLOMERATES,
            PrudentialConglomerateSummarySchema,
            "data/processed/prudential_conglomerates/summary/2014-03.csv",
            [("instituicao", 0), ("data_base", 8)],
        ),
        # --- Financial Conglomerates ---
        (
            InstitutionType.FINANCIAL_CONGLOMERATES,
            FinancialConglomeratesAssetsSchema,
            "data/processed/financial_conglomerates/assets/2004-12.csv",
            [("instituicao", 0), ("data_base", 8)],
        ),
        (
            InstitutionType.FINANCIAL_CONGLOMERATES,
            FinancialConglomerateLiabilitiesSchema,
            "data/processed/financial_conglomerates/liabilities/2000-03.csv",
            [("instituicao", 0), ("data_base", 8)],
        ),
        (
            InstitutionType.FINANCIAL_CONGLOMERATES,
            FinancialConglomerateIncomeStatementSchema,
            "data/processed/financial_conglomerates/income_statement/2000-03.csv",
            [("instituicao", 0), ("data_base", 8)],
        ),
        (
            InstitutionType.FINANCIAL_CONGLOMERATES,
            FinancialConglomerateSummarySchema,
            "data/processed/financial_conglomerates/summary/2000-03.csv",
            [("instituicao", 0), ("data_base", 8)],
        ),
        (
            InstitutionType.FINANCIAL_CONGLOMERATES,
            FinancialConglomerateCapitalInformationSchema,
            "data/processed/financial_conglomerates/capital_information/2000-12.csv",
            [("instituicao", 0), ("data_base", 8)],
        ),
        # --- Individual Institutions ---
        (
            InstitutionType.INDIVIDUAL_INSTITUTIONS,
            IndividualInstitutionAssetsSchema,
            "data/processed/individual_institutions/assets/2000-03.csv",
            # Schema uses 'instituicao' at 0, data_base at 10 (Legacy file structure)
            [("instituicao", 0), ("data_base", 10)],
        ),
        (
            InstitutionType.INDIVIDUAL_INSTITUTIONS,
            IndividualInstitutionLiabilitiesSchema,
            "data/processed/individual_institutions/liabilities/2000-03.csv",
            [("instituicao", 0), ("data_base", 10)],
        ),
        (
            InstitutionType.INDIVIDUAL_INSTITUTIONS,
            IndividualInstitutionIncomeStatementSchema,
            "data/processed/individual_institutions/income_statement/2000-03.csv",
            [("instituicao", 0), ("data_base", 10)],
        ),
        (
            InstitutionType.INDIVIDUAL_INSTITUTIONS,
            IndividualInstitutionSummarySchema,
            "data/processed/individual_institutions/summary/2000-03.csv",
            [("instituicao", 0), ("data_base", 10)],
        ),
        # --- Foreign Exchange ---
        (
            InstitutionType.FOREIGN_EXCHANGE,
            ForeignExchangeQuarterlyForeignCurrencyFlowSchema,
            "data/processed/foreign_exchange/quarterly_foreign_currency_flow/2015-09.csv",
            # Inst at 0, Data Base at 8
            [("instituicao", 0), ("data_base", 8)],
        ),
        # --- SCR Portfolio (Sample) ---
        (
            InstitutionType.FINANCIAL_CONGLOMERATES_SCR,
            FinancialConglomerateSCRPortfolioIndividualsTypeMaturitySchema,
            "data/processed/financial_conglomerates_scr/portfolio_individuals_type_maturity/2012-09.csv",
            # Debug dump showed: Inst at 0, Data Base at 9
            [("instituicao", 0), ("data_base", 9)],
        ),
    ],
)
@pytest.mark.transformation
def test_etl_integrity_sampling(controller, institution_type, schema_class, file_rel_path, key_fields):
    """Verifies that the ETL process (Controller + Schema) correctly loads a sample file
    without data corruption, comparing Raw text vs Transformed DataFrame.
    """

    file_path = Config.BASE_DIRECTORY / file_rel_path

    # Skip if file doesn't exist (local dev environment might vary)
    if not file_path.exists():
        pytest.skip(f"Test data file not found: {file_path}")

    schema = schema_class()

    # 1. Read Raw Truth
    # Processed files now include the normalized header as line 0.
    # Line 1 is the first data row.
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        if len(lines) < 2:
            pytest.skip("CSV file has no data rows")

        raw_row_list = lines[1].strip().split(';')

    # 2. Transform
    transformed_data_frame = controller.transform(file_path, schema, institution_type)
    assert not transformed_data_frame.empty, "Transformed DataFrame is empty"

    etl_row = transformed_data_frame.iloc[0]

    # 3. Dynamic Index Logic (for Prudenital Liabilities specifically)
    for field, default_raw_index in key_fields:
        # Handle the specific shift for Prudential Liabilities (Legacy check)
        target_idx = default_raw_index
        if institution_type == InstitutionType.PRUDENTIAL_CONGLOMERATES and "liabilities" in str(file_path):
            # Logic is handled by Controller, but we need to know WHERE to look in RAW file
            # If RAW has 30 cols, PL is at index 28. If 31, PL is at 29.
            # User passed 29 (Modern) in params.
            if len(raw_row_list) == 30 and default_raw_index > 28:
                target_idx = default_raw_index - 1

        # Check Bounds
        if target_idx >= len(raw_row_list):
            pytest.fail(
                f"Field {field} (index {target_idx}) is out of bounds for raw row with {len(raw_row_list)} columns"
            )

        # Get Raw
        raw_value = raw_row_list[target_idx]

        # Get ETL
        transformed_value = etl_row.get(field)

        # Convert Dates
        if field == 'data_base':
            # Raw: MM/YYYY -> ETL: YYYY-MM-DD
            if '/' in raw_value:
                month, year = raw_value.split('/')
                expected_date_str = f"{year}-{month}-01"
                etl_date_str = str(transformed_value).split(' ')[0]
                assert etl_date_str == expected_date_str, f"Date Mismatch: Raw {raw_value} vs ETL {transformed_value}"
                continue

        # Standard Compare
        normalized_raw_value = normalize_value(raw_value)
        normalized_transformed_value = normalize_value(transformed_value)

        assert (
            normalized_raw_value == normalized_transformed_value
        ), f"Value Mismatch for '{field}': Raw='{normalized_raw_value}' vs ETL='{normalized_transformed_value}'"
