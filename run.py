#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: run.py
#  Version: 0.0.1
#  Summary: Banco Central do Brasil IF.data Scraper
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
Banco Central do Brasil IF.data Scraper

This script is designed to automate the download of reports from the Banco Central do Brasil's
IF.data tool. It facilitates the integration with automated data analysis and visualization tools,
ensuring easy and timely access to data.

Author: Alexsander Lopes Camargos
License: MIT
"""

import bacen_ifdata_scraper.config as CONFIG
from bacen_ifdata_scraper.session import Session
from bacen_ifdata_scraper.utils import (initialize_webdriver,
                                        build_directory_path,
                                        ensure_directory,
                                        wait_for_download_completion)
from bacen_ifdata_scraper.storage.processing import process_downloaded_files
from bacen_ifdata_scraper.institutions_type import InstitutionType as INSTITUTION
from bacen_ifdata_scraper.reports_type import REPORTS
from bacen_ifdata_scraper.exceptions import IfDataScraperException


def main_scraper(_session: Session, _data_base: str, _institution, _report):
    """Main function for the scraper."""

    # Ensure that the download directory exists.
    ensure_directory(build_directory_path(CONFIG.DOWNLOAD_DIRECTORY))

    # Create the directory for the institution and report.
    institution_directory = build_directory_path(CONFIG.DOWNLOAD_DIRECTORY, _institution.name.lower())
    ensure_directory(institution_directory)
    report_directory = build_directory_path(institution_directory, _report.name.lower())
    ensure_directory(report_directory)

    # Download the reports.
    _session.download_reports(_data_base, _institution, _report)

    # Wait for the download to finish before processing the file.
    if wait_for_download_completion(CONFIG.DOWNLOAD_DIRECTORY,
                                    CONFIG.DOWNLOAD_FILE_NAME):
        report_file_path = build_directory_path(CONFIG.DOWNLOAD_DIRECTORY,
                                                _institution.name.lower(),
                                                _report.name.lower(),
                                                f'{_data_base.replace('/', '_')}.csv')

        process_downloaded_files(build_directory_path(CONFIG.DOWNLOAD_DIRECTORY,
                                                      CONFIG.DOWNLOAD_FILE_NAME
                                                      ),
                                 report_file_path)
    else:
        print('Download was not completed in the expected time.')


if __name__ == '__main__':
    session = None

    # Institution and report to be downloaded.
    institution = INSTITUTION.FINANCIAL_CONGLOMERATES
    report = REPORTS[institution].PORTFOLIO_NUMBER_CLIENTS_OPERATIONS

    try:
        # Initialize the WebDriver session.
        with initialize_webdriver() as driver:
            session = Session(driver, CONFIG.URL)
            session.open()

            # Get the available data bases.
            data_base = session.get_data_bases()

            # Download the reports.
            main_scraper(session, data_base[0], institution, report)
    except IfDataScraperException as error:
        print(error.message)
    finally:
        # Clean up the session, closing the browser and show report.
        if session:
            session.cleanup()
