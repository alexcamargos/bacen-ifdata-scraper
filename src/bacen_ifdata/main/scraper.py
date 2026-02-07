#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: scraper.py
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
from time import sleep

from loguru import logger

from bacen_ifdata.interfaces import SessionProtocol
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.storage.processing import (
    build_directory_path,
    check_file_already_downloaded,
    ensure_directory,
    process_downloaded_files,
    wait_for_download_completion,
)
from bacen_ifdata.utilities.configurations import Config as Cfg


def main(session: SessionProtocol, report_date: str, institution: Institutions, report: StrEnum) -> None:
    """Main function for the scraper.

    This function orchestrates the scraping process for the reports
    downloaded from the Banco Central do Brasil's IF.data tool.

    Args:
        session (SessionProtocol): The session object for the scraper.
        report_date (str): The base date for the reports to be downloaded.
        institution (Institutions): The institution for which the reports will be downloaded.
        report (Reports): The report that will be downloaded.
    """

    # Ensure that the download directory exists.
    ensure_directory(build_directory_path(Cfg.DOWNLOAD_DIRECTORY))

    # Create the directory for the institution and report.
    institution_directory = build_directory_path(Cfg.DOWNLOAD_DIRECTORY, institution.name.lower())
    ensure_directory(institution_directory)
    report_directory = build_directory_path(institution_directory, report.name.lower())
    ensure_directory(report_directory)

    # Build the name of the file that will contain the report, in the form 'year-month.csv'.
    month, year = report_date.split('/')
    report_file_name = f'{year}-{month}.csv'

    # Build the path to the report file.
    report_file_path = build_directory_path(
        Cfg.DOWNLOAD_DIRECTORY, institution.name.lower(), report.name.lower(), report_file_name
    )

    # Check if the file was already downloaded.
    if check_file_already_downloaded(report_file_path):
        logger.info(
            f'Report "{report.name}" from "{institution.name}" referring to "{report_date}" was already downloaded, skipping...'
        )
    else:
        # Download the reports.
        session.download_reports(report_date, institution, report)

        # Wait for the download to finish before processing the file.
        if wait_for_download_completion(Cfg.DOWNLOAD_DIRECTORY, Cfg.DOWNLOAD_FILE_NAME):
            sleep(3)
            process_downloaded_files(
                build_directory_path(Cfg.DOWNLOAD_DIRECTORY, Cfg.DOWNLOAD_FILE_NAME), report_file_path
            )
        else:
            logger.error('Download was not completed in the expected time.')
