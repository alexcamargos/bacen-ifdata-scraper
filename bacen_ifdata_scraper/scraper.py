#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: scraper.py
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
Este sistema foi projetado para automatizar o download dos relatórios da ferramenta
IF.data do Banco Central do Brasil. Criado para facilitar a integração com ferramentas
automatizadas de análise e visualização de dados, garantido acesso fácil e oportuno aos dados.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

from bacen_ifdata_scraper import config
from bacen_ifdata_scraper.utils import ensure_clickable


def download_ifdata_reports(driver: webdriver,
                            data_base: str,
                            institution_type: str,
                            report_type: str):
    """
    Navigates to the financial reports page of the Central Bank of Brazil using a WebDriver,
    interacts with the page to select the desired options for data base, type of institution,
    and type of report, and initiates the download process for the report in CSV format.

    The function dynamically waits until the necessary elements are clickable and interacts
    with multiple dropdown menus to set the report criteria specified by the parameters.

    Parameters:
        driver (webdriver): Instance of the browser's WebDriver.
        data_base (str): Base date of the report available for download.
        institution_type (str): Type of financial institution for which the report is desired.
        report_type (str): Type of report to be downloaded.

    Behavior:
        The function performs a series of actions to interact with the web page:
        1. Accesses the URL of the financial reports.
        2. Waits and interacts with the data base selection menu.
        3. Waits and interacts with the type of institution selection menu.
        4. Waits and interacts with the type of report selection menu.
        5. Initiates the download of the selected report.

    Notes:
        - The function relies on external configuration (config.py) for URLs and timeouts.
        - The implementation assumes that the page and its elements are in an expected state and may
          require updates if the site structure of the Central Bank of Brazil changes.
        - Checking for the completion of the file download still needs to be implemented (TODO).

    Returns:
        None. The function initiates the file download but does not verify its completion.
    """

    # Acesse a página onde estão os relatórios.
    driver.get(config.URL)

    # IMPORTANTE: O sistema gera os relatórios de forma dinâmica, então precisamos
    # garantir que o conteúdo da página esteja carregado antes de prosseguir.
    # Para isso, vamos usar a função ensure_clickable() para garantir que o conteúdo
    # esteja carregado antes de prosseguirmos.

    # Forçando o inicio do carregando do conteúdo do dropdown menu "ulDataBase".
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'btnDataBase')

    # Garanta que o conteúdo do dropdown menu "ulDataBase" esteja carregado antes de prosseguir.
    ensure_clickable(driver,
                     config.TIMEOUT,
                     By.XPATH,
                     f"//a[text()='{data_base}']")

    # Forçando o inicio do carregando do conteúdo do dropdown menu "ulTipoInst".
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'btnTipoInst')

    # Garanta que o conteúdo do dropdown menu "ulTipoInst" esteja carregado antes de prosseguir.
    ensure_clickable(driver,
                     config.TIMEOUT,
                     By.XPATH,
                     f"//a[text()='{institution_type}']")

    # Forçando o inicio do carregando do conteúdo do dropdown menu "ulRelatorio".
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'btnRelatorio')

    # Garanta que o conteúdo do dropdown menu "ulRelatorio" esteja carregado antes de prosseguir.
    ensure_clickable(driver,
                     config.TIMEOUT,
                     By.XPATH,
                     f"//a[text()='{report_type}']")

    # Garanta que o conteúdo do relatório esteja carregado antes de
    # prosseguir com o download do arquivo CSV.
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'aExportCsv')
