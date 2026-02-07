#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: transformer.py
#  Version: 0.0.1
#  Summary: Bacen IF.data AutoScraper & Data Manager
#           Este sistema foi projetado para automatizar o download dos
#           relatórios da ferramenta IF.data do Banco Central do Brasil.
#           Criado para facilitar a integração com ferramentas automatizadas de
#           análise e visualização de dados, garantido acesso fácil e oportuno
#           aos dados.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
#  ------------------------------------------------------------------------------

"""
Bacen IF.data AutoScraper & Data Manager

This script is designed to automate the download of reports from the Banco Central do Brasil's
IF.data tool. It facilitates the integration with automated data analysis and visualization tools,
ensuring easy and timely access to data.

Author: Alexsander Lopes Camargos
License: MIT
"""

from enum import StrEnum
from pathlib import Path
from typing import Final

import pandas as pd
from loguru import logger

from bacen_ifdata.data_transformer.interfaces.controller import TransformerControllerInterface
from bacen_ifdata.data_transformer.schemas import (
    # Prudential Conglomerate schemas
    PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA,
    PRUDENTIAL_CONGLOMERATE_CAPITAL_INFORMATION_SCHEMA,
    PRUDENTIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA,
    PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA,
    PRUDENTIAL_CONGLOMERATE_SEGMENTATION_SCHEMA,
    PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA,
    # Financial Conglomerates schemas
    FINANCIAL_CONGLOMERATE_ASSETS_SCHEMA,
    FINANCIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA,
    FINANCIAL_CONGLOMERATE_LIABILITIES_SCHEMA,
    FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA,
    FINANCIAL_CONGLOMERATE_PORTFOLIO_INDIVIDUALS_TYPE_MATURITY_SCHEMA,
    FINANCIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY_SCHEMA,
    FINANCIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY_SCHEMA,
    FINANCIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE_SCHEMA,
    FINANCIAL_CONGLOMERATE_PORTFOLIO_NUMBER_CLIENTS_OPERATIONS_SCHEMA,
    FINANCIAL_CONGLOMERATE_PORTFOLIO_RISK_LEVEL_SCHEMA,
    FINANCIAL_CONGLOMERATE_PORTFOLIO_INDEXER_SCHEMA,
    FINANCIAL_CONGLOMERATE_PORTFOLIO_GEOGRAPHIC_REGION_SCHEMA,
    # Individual Institutions schemas
    INDIVIDUAL_INSTITUTION_ASSETS_SCHEMA,
    INDIVIDUAL_INSTITUTION_INCOME_STATEMENT_SCHEMA,
    INDIVIDUAL_INSTITUTION_LIABILITIES_SCHEMA,
    INDIVIDUAL_INSTITUTION_SUMMARY_SCHEMA,
)
from bacen_ifdata.data_transformer.schemas.interfaces import SchemaProtocol
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import (
    ReportsFinancialConglomerates,
    ReportsIndividualInstitutions,
    ReportsPrudentialConglomerates,
)
from bacen_ifdata.scraper.storage.processing import build_directory_path, ensure_directory
from bacen_ifdata.utilities.configurations import Config as Cfg


def store_transformed_data(transformed_data: pd.DataFrame, output_directory: Path, file_name: str) -> None:
    """Save the transformed data to the output directory.

    This function saves the transformed data to a CSV file in the specified
    output directory.

    Arguments:
        transformed_data (pd.DataFrame): The transformed data to be saved.
        output_directory (Path): The directory where the data should be saved.
        file_name (str): The name of the file to save the data as.
    """

    transformed_data.to_csv(output_directory / file_name, index=False)
    logger.info(f'Successfully transformed: {output_directory / file_name}')


# Schema mapping by institution and report type.
SCHEMA_BY_INSTITUTION_AND_REPORT: Final[dict[Institutions, dict[StrEnum, SchemaProtocol]]] = {
    Institutions.PRUDENTIAL_CONGLOMERATES: {
        ReportsPrudentialConglomerates.SUMMARY: PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA,
        ReportsPrudentialConglomerates.ASSETS: PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA,
        ReportsPrudentialConglomerates.LIABILITIES: PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA,
        ReportsPrudentialConglomerates.INCOME_STATEMENT: PRUDENTIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA,
        ReportsPrudentialConglomerates.CAPITAL_INFORMATION: PRUDENTIAL_CONGLOMERATE_CAPITAL_INFORMATION_SCHEMA,
        ReportsPrudentialConglomerates.SEGMENTATION: PRUDENTIAL_CONGLOMERATE_SEGMENTATION_SCHEMA,
    },
    Institutions.FINANCIAL_CONGLOMERATES: {
        ReportsFinancialConglomerates.SUMMARY: FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA,
        ReportsFinancialConglomerates.ASSETS: FINANCIAL_CONGLOMERATE_ASSETS_SCHEMA,
        ReportsFinancialConglomerates.LIABILITIES: FINANCIAL_CONGLOMERATE_LIABILITIES_SCHEMA,
        ReportsFinancialConglomerates.INCOME_STATEMENT: FINANCIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA,
        ReportsFinancialConglomerates.PORTFOLIO_INDIVIDUALS_TYPE_MATURITY: FINANCIAL_CONGLOMERATE_PORTFOLIO_INDIVIDUALS_TYPE_MATURITY_SCHEMA,
        ReportsFinancialConglomerates.PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY: FINANCIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY_SCHEMA,
        ReportsFinancialConglomerates.PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY: FINANCIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY_SCHEMA,
        ReportsFinancialConglomerates.PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE: FINANCIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE_SCHEMA,
        ReportsFinancialConglomerates.PORTFOLIO_NUMBER_CLIENTS_OPERATIONS: FINANCIAL_CONGLOMERATE_PORTFOLIO_NUMBER_CLIENTS_OPERATIONS_SCHEMA,
        ReportsFinancialConglomerates.PORTFOLIO_RISK_LEVEL: FINANCIAL_CONGLOMERATE_PORTFOLIO_RISK_LEVEL_SCHEMA,
        ReportsFinancialConglomerates.PORTFOLIO_INDEXER: FINANCIAL_CONGLOMERATE_PORTFOLIO_INDEXER_SCHEMA,
        ReportsFinancialConglomerates.PORTFOLIO_GEOGRAPHIC_REGION: FINANCIAL_CONGLOMERATE_PORTFOLIO_GEOGRAPHIC_REGION_SCHEMA,
    },
    Institutions.INDIVIDUAL_INSTITUTIONS: {
        ReportsIndividualInstitutions.SUMMARY: INDIVIDUAL_INSTITUTION_SUMMARY_SCHEMA,
        ReportsIndividualInstitutions.ASSETS: INDIVIDUAL_INSTITUTION_ASSETS_SCHEMA,
        ReportsIndividualInstitutions.LIABILITIES: INDIVIDUAL_INSTITUTION_LIABILITIES_SCHEMA,
        ReportsIndividualInstitutions.INCOME_STATEMENT: INDIVIDUAL_INSTITUTION_INCOME_STATEMENT_SCHEMA,
    },
}


def main(transformer_controller: TransformerControllerInterface, institution: Institutions, report: StrEnum) -> None:
    """Main function for the transformer.

    This function orchestrates the transformation process for the reports
    downloaded from the Banco Central do Brasil's IF.data tool.

    Arguments:
        transformer_controller (TransformerControllerInterface): The transformer controller.
        institution (Institutions): The institution type.
        report (StrEnum): The report type.
    """

    # Check if we have schemas for this institution.
    if institution not in SCHEMA_BY_INSTITUTION_AND_REPORT:
        logger.warning(f'No schema mapping found for institution: {institution.name}. Skipping transformation.')
        return

    # Get the schema mapping for this institution.
    schema_by_report = SCHEMA_BY_INSTITUTION_AND_REPORT[institution]

    # Ensure that the transformed files directory exists.
    output_directory = build_directory_path(
        Cfg.TRANSFORMED_FILES_DIRECTORY, institution.name.lower(), report.name.lower()
    )
    ensure_directory(output_directory)

    # Build the path to the input data directory.
    input_data_path = build_directory_path(Cfg.PROCESSED_FILES_DIRECTORY, institution.name.lower(), report.name.lower())

    # Get the schema for the report.
    report_schema = schema_by_report.get(report)
    if report_schema is None:
        logger.warning(f'No schema found for report: {report.name} in {institution.name}. Skipping.')
        return

    # List all CSV files in the input data directory.
    for file in input_data_path.glob('*.csv'):
        logger.info(f'Transforming {report.name} ({file.name}) from {institution.name}.')
        # Transform the CSV file.
        transformed_data = transformer_controller.transform(file, report_schema, institution)
        # Save the transformed data to the output directory.
        store_transformed_data(transformed_data, output_directory, file.name)
