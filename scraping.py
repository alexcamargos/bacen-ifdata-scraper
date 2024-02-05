#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: scraping.py
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

from time import sleep
import bacen_ifdata.utilities.config as config
from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.institutions import InstitutionType as INSTITUTIONS
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.scraper.session import Session
from bacen_ifdata.scraper.storage.processing import (process_downloaded_files,
                                                     build_directory_path,
                                                     ensure_directory,
                                                     wait_for_download_completion,
                                                     check_file_already_downloaded)
from bacen_ifdata.scraper.utils import (initialize_webdriver,
                                        validate_report_selection)
from bacen_ifdata.utilities.clean import (clean_empty_csv_files,
                                          clean_download_base_directory)


def __clean_download_directory():
    """
    Performs comprehensive cleaning operations on the download directory.

    This function orchestrates a two-step cleaning process:
    1. It first removes all empty CSV files from the download directory.
       This step helps in eliminating files that were downloaded but contain
       no data, possibly due to errors in the data scraping process.
    2. Then, it cleans up the download base directory by removing any
       remaining CSV files. This is typically done to prepare for a fresh start,
       ensuring that no outdated or unnecessary files remain that could interfere
       with subsequent scraping sessions.

    The cleaning process targets the directory specified in the configuration's DOWNLOAD_DIRECTORY,
    using paths built from the configuration settings. Messages are printed to the console to
    indicate the progress of cleaning operations.
    """

    # Clean up the empty CSV files in the download directory.
    print('Cleaning up empty CSV files...')
    clean_empty_csv_files(build_directory_path(config.DOWNLOAD_DIRECTORY))
    # Clean up the download base directory.
    print('Cleaning up the download base directory...')
    clean_download_base_directory(
        build_directory_path(config.DOWNLOAD_DIRECTORY))


def main_scraper(_session: Session, _data_base: str, _institution, _report):
    """Main function for the scraper."""

    # Ensure that the download directory exists.
    ensure_directory(build_directory_path(config.DOWNLOAD_DIRECTORY))

    # Create the directory for the institution and report.
    institution_directory = build_directory_path(config.DOWNLOAD_DIRECTORY,
                                                 _institution.name.lower())
    ensure_directory(institution_directory)
    report_directory = build_directory_path(
        institution_directory, _report.name.lower())
    ensure_directory(report_directory)

    # Build the name of the file that will contain the report,
    # in the form 'year-month.csv'.
    month, year = _data_base.split('/')
    report_file_name = f'{year}-{month}.csv'

    # Build the path to the report file.
    report_file_path = build_directory_path(config.DOWNLOAD_DIRECTORY,
                                            _institution.name.lower(),
                                            _report.name.lower(),
                                            report_file_name)

    # Check if the file was already downloaded.
    if check_file_already_downloaded(report_file_path):
        print(f'Report "{_report.name}" from "{_institution.name}"'
              f'referring to "{_data_base}" was already downloaded, skipping...')
    else:
        # Download the reports.
        _session.download_reports(_data_base, _institution, _report)

        # Wait for the download to finish before processing the file.
        if wait_for_download_completion(config.DOWNLOAD_DIRECTORY,
                                        config.DOWNLOAD_FILE_NAME):
            sleep(3)
            process_downloaded_files(build_directory_path(config.DOWNLOAD_DIRECTORY,
                                                          config.DOWNLOAD_FILE_NAME),
                                     report_file_path)
        else:
            print('Download was not completed in the expected time.')


if __name__ == '__main__':
    session = None
    try:
        # Initialize the WebDriver session.
        with initialize_webdriver() as driver:
            session = Session(driver, config.URL)
            session.open()

            # Get the available data bases.
            data_base = session.get_data_bases()

            for institution in INSTITUTIONS:
                for report in REPORTS[institution]:
                    # Validate the report selection.
                    cutoff_data_base = validate_report_selection(institution,
                                                                 report,
                                                                 data_base)

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

    # BUG: The IF.data system generates CSV files for download in real-time,
    # using the loaded data table as the foundation.
    # Internally, it triggers the `downloadCsv` JavaScript function, which
    # constructs a Blob object of type "text/csv" and saves this file.
    # I have not been able to find a permanent solution to this issue.
    #
    # A temporary measure is to delete the empty files and rerun the
    # data scraping process, repeating this step until there are no
    # more content-less files remaining.
    __clean_download_directory()
