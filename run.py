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
from bacen_ifdata_scraper.utils import initialize_webdriver
from bacen_ifdata_scraper.utils import ensure_download_directory
from bacen_ifdata_scraper.utils import wait_for_download_completion
from bacen_ifdata_scraper.storage.processing import process_downloaded_files
from bacen_ifdata_scraper.institutions_type import InstitutionType as Institution
from bacen_ifdata_scraper.reports_type import REPORTS


if __name__ == '__main__':
    driver = initialize_webdriver()

    session = Session(driver, CONFIG.URL)
    session.open()

    # Ensure that the download directory exists.
    ensure_download_directory(CONFIG.DOWNLOAD_DIRECTORY)

    data_base = session.get_data_bases()

    session.download_reports(data_base[0],
                             Institution.FINANCIAL_CONGLOMERATES,
                             REPORTS[Institution.FINANCIAL_CONGLOMERATES]
                             .PORTFOLIO_NUMBER_CLIENTS_OPERATIONS,
                             )

    # Wait for the download to finish before processing the file.
    if wait_for_download_completion(CONFIG.DOWNLOAD_DIRECTORY, 'dados.csv'):
        process_downloaded_files(
            'dados.csv', f'{data_base[0].replace('/', '_')}.csv')
    else:
        print('Download was not completed in the expected time.')

    # Clean up the session, closing the browser and show report.
    session.cleanup()
