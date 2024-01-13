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
                                        validate_report_selection)
from bacen_ifdata_scraper.storage.processing import (process_downloaded_files,
                                                     build_directory_path,
                                                     ensure_directory,
                                                     wait_for_download_completion,
                                                     check_file_already_downloaded)
from bacen_ifdata_scraper.institutions import InstitutionType as INSTITUTIONS
from bacen_ifdata_scraper.reports import REPORTS
from bacen_ifdata_scraper.exceptions import IfDataScraperException


def main_scraper(_session: Session, _data_base: str, _institution, _report):
    """Main function for the scraper."""

    # Ensure that the download directory exists.
    ensure_directory(build_directory_path(CONFIG.DOWNLOAD_DIRECTORY))

    # Create the directory for the institution and report.
    institution_directory = build_directory_path(CONFIG.DOWNLOAD_DIRECTORY,
                                                 _institution.name.lower())
    ensure_directory(institution_directory)
    report_directory = build_directory_path(institution_directory, _report.name.lower())
    ensure_directory(report_directory)

    report_file_path = build_directory_path(CONFIG.DOWNLOAD_DIRECTORY,
                                            _institution.name.lower(),
                                            _report.name.lower(),
                                            f'{_data_base.replace('/', '_')}.csv')

    # Check if the file was already downloaded.
    if check_file_already_downloaded(report_file_path):
        print(f'Report "{_report.name}" from "{_institution.name}" referring to "{
            _data_base}" was already downloaded, skipping...')
    else:
        # Download the reports.
        _session.download_reports(_data_base, _institution, _report)

        # Wait for the download to finish before processing the file.
        if wait_for_download_completion(CONFIG.DOWNLOAD_DIRECTORY,
                                        CONFIG.DOWNLOAD_FILE_NAME):
            process_downloaded_files(build_directory_path(CONFIG.DOWNLOAD_DIRECTORY,
                                                          CONFIG.DOWNLOAD_FILE_NAME),
                                     report_file_path)
        else:
            print('Download was not completed in the expected time.')


if __name__ == '__main__':
    session = None
    try:
        # Initialize the WebDriver session.
        with initialize_webdriver() as driver:
            session = Session(driver, CONFIG.URL)
            session.open()

            # Get the available data bases.
            data_base = session.get_data_bases()

            for institution in INSTITUTIONS:
                for report in REPORTS[institution]:
                    # Validate the report selection.
                    cutoff_data_base = validate_report_selection(institution, report, data_base)

                    for data in cutoff_data_base:
                        # Download the reports.
                        print(f'Downloading report "{report.name}" from "{institution.name}" '
                              f'referring to "{data}"...')
                        main_scraper(session, data, institution, report)
    except IfDataScraperException as error:
        print(error.message)
    finally:
        # Clean up the session, closing the browser and show report.
        if session:
            session.cleanup()
