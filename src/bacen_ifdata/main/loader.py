#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: main.py
#  Version: 0.0.1
#
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
# ------------------------------------------------------------------------------

"""
Bacen IF.data AutoScraper & Data Manager

This script is designed to automate the download of reports from the Banco Central do Brasil's
IF.data tool. It facilitates the integration with automated data analysis and visualization tools,
ensuring easy and timely access to data.

Author: Alexsander Lopes Camargos
License: MIT
"""

from enum import StrEnum

from loguru import logger

from bacen_ifdata.data_loader.controller import LoaderController
from bacen_ifdata.data_transformer.schemas.mapper import SCHEMA_BY_INSTITUTION_AND_REPORT
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.storage.processing import build_directory_path
from bacen_ifdata.utilities.configurations import Config as Cfg


def main(institution: Institutions, report: StrEnum) -> None:
    """Main function for the transformer.

    This function orchestrates the loading process for the reports
    downloaded from the Banco Central do Brasil's IF.data tool.

    Args:
        institution (Institutions): The institution for which the reports will be loaded.
        report (StrEnum): The report that will be loaded.
    """

    # Check if we have schemas for this institution.
    if institution not in SCHEMA_BY_INSTITUTION_AND_REPORT:
        logger.warning(f'No schema mapping found for institution: {institution.name}. Skipping loading.')
        return

    # Get the schema for the report.
    schema_by_report = SCHEMA_BY_INSTITUTION_AND_REPORT[institution]
    report_schema = schema_by_report.get(report)
    if report_schema is None:
        logger.warning(f'No schema found for report: {report.name} in {institution.name}. Skipping.')
        return

    # Build the path to the input data directory.
    input_data_path = build_directory_path(
        Cfg.TRANSFORMED_FILES_DIRECTORY, institution.name.lower(), report.name.lower()
    )
    # Create the controller object.
    controller = LoaderController()

    # List all CSV files in the input data directory.
    for file in input_data_path.glob('*.csv'):
        logger.info(f'Loading {report.name} ({file.name}) from {institution.name}.')
        # Load the data into the database.
        controller.load_report(institution, report, file, report_schema)
