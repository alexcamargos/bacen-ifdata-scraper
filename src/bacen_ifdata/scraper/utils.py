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

from enum import StrEnum

from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    MoveTargetOutOfBoundsException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.utilities.configurations import Config as Cfg


def ensure_clickable(driver: WebDriver, wait_time: int, by_method: By, locator: str) -> None:
    """
    Waits for an element to be clickable on a web page and then clicks it.

    Args:
        driver (WebDriver): The WebDriver instance for browser interactions.
        wait_time (int): The maximum time to wait for the element to become clickable.
        by_method (By): The Selenium By method to locate the element.
        locator (str): The locator string for finding the element.

    Raises:
        TimeoutException: If the element doesn't become clickable after wait_time seconds.
        NoSuchElementException: If the element is not found on the page.
        ElementClickInterceptedException: If the element is intercepted by another element.
        MoveTargetOutOfBoundsException: If the element is outside the boundaries of the window.
    """

    try:
        # Convert by_method to string if it's a By object
        by_method_str = str(by_method) if not isinstance(by_method, str) else by_method
        # Wait until the element is clickable.
        element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((by_method_str, locator)))
        # Click the element using JavaScript.
        driver.execute_script('arguments[0].click();', element)

    except TimeoutException:
        logger.exception(
            f'Timeout: O elemento {
                         locator} não se tornou clicável após {wait_time} segundos.'
        )
        raise
    except NoSuchElementException:
        logger.exception(
            f'Não encontrado: O elemento {
                         locator} não foi encontrado na página.'
        )
        raise
    except ElementClickInterceptedException:
        logger.exception(
            f'Elemento interceptado: O elemento {
                         locator} foi interceptado por outro elemento.'
        )
        raise
    except MoveTargetOutOfBoundsException:
        logger.exception(
            f'Fora dos limites: O elemento {
                         locator} está fora dos limites da janela.'
        )
        raise


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
    options.set_preference("browser.download.dir", str(Cfg.DOWNLOAD_DIRECTORY))
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # Initializes the WebDriver for Firefox.
    driver = webdriver.Firefox(options=options)

    return driver


def validate_report_selection(institution: Institutions, report: StrEnum, data_base: list[str]) -> list[str]:
    """Validates the report selection."""

    if institution == Institutions.PRUDENTIAL_CONGLOMERATES and report in (
        REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].SUMMARY,
        REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].ASSETS,
        REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].LIABILITIES,
        REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].INCOME_STATEMENT,
    ):
        cutoff_date = '03/2014'
    elif (
        institution == Institutions.PRUDENTIAL_CONGLOMERATES
        and report == REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].CAPITAL_INFORMATION
    ):
        cutoff_date = '03/2015'
    elif (
        institution == Institutions.PRUDENTIAL_CONGLOMERATES
        and report == REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].SEGMENTATION
    ):
        cutoff_date = '03/2017'
    elif institution == Institutions.FINANCIAL_CONGLOMERATES and report in (
        REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_INDIVIDUALS_TYPE_MATURITY,
        REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY,
        REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY,
        REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE,
        REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_NUMBER_CLIENTS_OPERATIONS,
        REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_RISK_LEVEL,
        REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_INDEXER,
    ):
        cutoff_date = '06/2014'
    elif (
        institution == Institutions.FINANCIAL_CONGLOMERATES
        and report == REPORTS[Institutions.FINANCIAL_CONGLOMERATES].PORTFOLIO_GEOGRAPHIC_REGION
    ):
        cutoff_date = '09/2014'
    elif (
        institution == Institutions.FINANCIAL_CONGLOMERATES
        and report == REPORTS[Institutions.FINANCIAL_CONGLOMERATES].CAPITAL_INFORMATION
    ):
        cutoff_date_start = '12/2000'
        data_base_index_start = data_base.index(cutoff_date_start)

        cutoff_date_end = '12/2014'
        data_base_index_end = data_base.index(cutoff_date_end)

        return data_base[data_base_index_end : data_base_index_start + 1]
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
        return data_base[: data_base_index + 1]
    except ValueError:
        # cutoff_date not in data_base, return as is
        return data_base
