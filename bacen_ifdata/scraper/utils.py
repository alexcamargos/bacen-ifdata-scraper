#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: utils.py
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
Utility functions for Bacen IF.data AutoScraper & Data Manager

This module provides utility functions for initializing a WebDriver session with Firefox,
which is used to interact with web pages.

Author: Alexsander Lopes Camargos
License: MIT
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.utilities.configurations import Config as Cfg


def initialize_webdriver() -> WebDriver:
    """
    Initializes a WebDriver session with Firefox.

    Returns:
        WebDriver: The WebDriver instance being used to interact with the web page.
    """

    # Configures the options for the WebDriver.
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    # Set the directory where the downloaded files will be stored.
    options.set_preference("browser.download.dir",
                           str(Cfg.DOWNLOAD_DIRECTORY.value))
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # Initializes the WebDriver for Firefox.
    driver = webdriver.Firefox(options=options)

    return driver


def validate_report_selection(institution: str, report: str, data_base: list) -> list:
    """Validates the report selection."""

    if institution == Institutions.PRUDENTIAL_CONGLOMERATES and \
        report in (REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].SUMMARY,
                   REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].ASSETS,
                   REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].LIABILITIES,
                   REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].INCOME_STATEMENT):
        cutoff_date = '03/2014'
    elif institution == Institutions.PRUDENTIAL_CONGLOMERATES and \
            report == REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].CAPITAL_INFORMATION:
        cutoff_date = '03/2015'
    elif institution == Institutions.PRUDENTIAL_CONGLOMERATES and \
            report == REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].SEGMENTATION:
        cutoff_date = '03/2017'
    elif institution == Institutions.FINANCIAL_CONGLOMERATES and \
            report in (REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_INDIVIDUALS_TYPE_MATURITY,
                       REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY,
                       REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY,
                       REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE,
                       REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_NUMBER_CLIENTS_OPERATIONS,
                       REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_RISK_LEVEL,
                       REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_INDEXER):
        cutoff_date = '06/2014'
    elif institution == Institutions.FINANCIAL_CONGLOMERATES and \
            report == REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_GEOGRAPHIC_REGION:
        cutoff_date = '09/2014'
    elif institution == Institutions.FINANCIAL_CONGLOMERATES and \
            report == REPORTS[Institutions.FINANCIAL_CONGLOMERATES].CAPITAL_INFORMATION:
        cutoff_date_start = '12/2000'
        data_base_index_start = data_base.index(cutoff_date_start)

        cutoff_date_end = '12/2014'
        data_base_index_end = data_base.index(cutoff_date_end)

        return data_base[data_base_index_end:data_base_index_start + 1]
    elif institution == Institutions.FOREIGN_EXCHANGE:
        cutoff_date_start = '12/2014'

        data_base_index_start = data_base.index(cutoff_date_start)

        cutoff_date_end = '06/2023'
        data_base_index_end = data_base.index(cutoff_date_end)

        return data_base[data_base_index_end:data_base_index_start]
    elif institution == Institutions.FINANCIAL_CONGLOMERATES_SCR:
        cutoff_date_start = '06/2012'
        data_base_index_start = data_base.index(cutoff_date_start)

        cutoff_date_end = '03/2014'
        data_base_index_end = data_base.index(cutoff_date_end)

        return data_base[data_base_index_end:data_base_index_start]
    else:
        # No cutoff for other institutions and reports.
        return data_base

    try:
        data_base_index = data_base.index(cutoff_date)
        return data_base[:data_base_index + 1]
    except ValueError:
        # cutoff_date not in data_base, return as is
        return data_base
