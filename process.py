#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: process.py
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

"""Bacen IF.data AutoScraper & Data Manager"""

from enum import StrEnum

import bacen_ifdata.config as CONFIG

from bacen_ifdata.data_manager.processing import normalize_csv
from bacen_ifdata.scraper.institutions import InstitutionType as INSTITUTIONS
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.scraper.storage.processing import (ensure_directory,
                                                     build_directory_path)


def main_process(institution: StrEnum, report: StrEnum) -> None:
    """Main process for Bacen IF.data AutoScraper & Data Manager"""

    # Ensure that the processed files directory exists.
    output_directory = build_directory_path(CONFIG.PROCESSED_FILES_DIRECTORY,
                                            institution.name.lower(),
                                            report.name.lower())
    ensure_directory(output_directory)

    input_data_path = build_directory_path(CONFIG.DOWNLOAD_DIRECTORY,
                                           institution.name.lower(),
                                           report.name.lower())
    # List all CSV files in the input data directory.
    for file in input_data_path.glob('*.csv'):
        print(f'Normalizing {report.name} ({
              file.name}) from {institution.name}.')
        # Normalize the CSV file.
        normalize_csv(institution, report, file.name)


if __name__ == '__main__':

    # Ensure that the processed files directory exists.
    ensure_directory(build_directory_path(CONFIG.PROCESSED_FILES_DIRECTORY))

    # Run the main process.
    for process_institution in INSTITUTIONS:
        for process_report in REPORTS[process_institution]:
            main_process(process_institution, process_report)
