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

from os import getenv
from pathlib import Path
from shutil import which

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
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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

    # Handle exceptions and log them appropriately.
    except TimeoutException:
        logger.exception(f'Timeout: O elemento {locator} não se tornou clicável após {wait_time} segundos.')
        raise
    except NoSuchElementException:
        logger.exception(f'Não encontrado: O elemento {locator} não foi encontrado na página.')
        raise
    except ElementClickInterceptedException:
        logger.exception(f'Elemento interceptado: O elemento {locator} foi interceptado por outro elemento.')
        raise
    except MoveTargetOutOfBoundsException:
        logger.exception(f'Fora dos limites: O elemento {locator} está fora dos limites da janela.')
        raise


def initialize_webdriver(download_directory: Path) -> WebDriver:
    """Initialize a Firefox profile with a dedicated download directory.

    Args:
        download_directory: Location for this profile's downloads.

    Returns:
        The Firefox WebDriver.

    Raises:
        WebDriverException: If Firefox cannot be started.
    """

    # Configures the options for the WebDriver.
    options = Options()
    options.page_load_strategy = 'eager'
    firefox_binary = getenv('IFDATA_FIREFOX_BINARY')
    if firefox_binary:
        options.binary_location = firefox_binary
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    # Set the directory where the downloaded files will be stored.
    options.set_preference("browser.download.dir", str(download_directory))
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # Use Selenium Manager when Firefox or geckodriver needs discovery.
    executable = which('geckodriver')
    service = None
    if firefox_binary and executable:
        service = Service(executable_path=executable)
    return webdriver.Firefox(options=options, service=service)
