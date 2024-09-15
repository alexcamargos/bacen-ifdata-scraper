#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: cleaner.py
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

from loguru import logger

from bacen_ifdata.data_manager.processing import normalize_csv
from bacen_ifdata.scraper.storage.processing import (build_directory_path,
                                                     ensure_directory)
from bacen_ifdata.utilities import config


def main(institution: StrEnum, report: StrEnum) -> None:
    """Main function for the cleaner.

    This function orchestrates the normalization process for the reports
    downloaded from the Banco Central do Brasil's IF.data tool.

    Args:
        institution (StrEnum): The institution for which the reports will be normalized.
        report (StrEnum): The report that will be normalized.
    """

    # Ensure that the processed files directory exists.
    output_directory = build_directory_path(config.PROCESSED_FILES_DIRECTORY,
                                            institution.name.lower(),
                                            report.name.lower())
    ensure_directory(output_directory)

    # Build the path to the input data directory.
    input_data_path = build_directory_path(config.DOWNLOAD_DIRECTORY,
                                           institution.name.lower(),
                                           report.name.lower())

    # List all CSV files in the input data directory.
    for file in input_data_path.glob('*.csv'):
        logger.info(f'Normalizing {report.name} ({file.name}) from {institution.name}.')
        # Normalize the CSV file.
        normalize_csv(institution, report, file.name)
