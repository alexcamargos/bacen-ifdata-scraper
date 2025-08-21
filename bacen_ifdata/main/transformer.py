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

import pandas as pd
from loguru import logger

from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.data_transformer.schemas import (PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA,
                                                   PRUDENTIAL_CONGLOMERATE_CAPITAL_INFORMATION_SCHEMA,
                                                   PRUDENTIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA,
                                                   PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA,
                                                   PRUDENTIAL_CONGLOMERATE_SEGMENTATION_SCHEMA,
                                                   PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import ReportsPrudentialConglomerates
from bacen_ifdata.scraper.storage.processing import (build_directory_path,
                                                     ensure_directory)
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


def main(institution: Institutions, report: StrEnum) -> None:
    """Main function for the transformer.

    This function orchestrates the transformation process for the reports
    downloaded from the Banco Central do Brasil's IF.data tool.

    Arguments:
        data_frame (pd.DataFrame): The data frame containing the report data.
    """

    # Create the controller instance.
    controller = TransformerController()

    # Ensure that the transformed files directory exists.
    output_directory = build_directory_path(Cfg.TRANSFORMED_FILES_DIRECTORY.value,
                                            institution.name.lower(),
                                            report.name.lower())
    ensure_directory(output_directory)

    # Build the path to the input data directory.
    input_data_path = build_directory_path(Cfg.PROCESSED_FILES_DIRECTORY.value,
                                           institution.name.lower(),
                                           report.name.lower())

    # Map report types to their schemas.
    schema_by_report = {
        ReportsPrudentialConglomerates.SUMMARY: PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA,
        ReportsPrudentialConglomerates.ASSETS: PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA,
        ReportsPrudentialConglomerates.LIABILITIES: PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA,
        ReportsPrudentialConglomerates.INCOME_STATEMENT: PRUDENTIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA,
        ReportsPrudentialConglomerates.CAPITAL_INFORMATION: PRUDENTIAL_CONGLOMERATE_CAPITAL_INFORMATION_SCHEMA,
        ReportsPrudentialConglomerates.SEGMENTATION: PRUDENTIAL_CONGLOMERATE_SEGMENTATION_SCHEMA,
    }

    # Run the transformation process.
    if institution == Institutions.PRUDENTIAL_CONGLOMERATES:
        # Get the schema for the report.
        report_schema = schema_by_report.get(ReportsPrudentialConglomerates(report))
        if report_schema is None:
            raise ValueError(f'No schema found for report: {report.name}')

        # List all CSV files in the input data directory.
        for file in input_data_path.glob('*.csv'):
            logger.info(f'Transforming {report.name} ({file.name}) from {institution.name}.')
            # Transform the CSV file.
            transformed_data = controller.transform(file, report_schema)
            # Save the transformed data to the output directory.
            store_transformed_data(transformed_data, output_directory, file.name)
