#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: utils.py
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
Utility functions for Banco Central do Brasil IF.data Scraper

This module provides utility functions for initializing a WebDriver session with Firefox,
which is used to interact with web pages.

Author: Alexsander Lopes Camargos
License: MIT
"""

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from bacen_ifdata_scraper.config import DOWNLOAD_DIRECTORY


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
    options.set_preference("browser.download.dir", DOWNLOAD_DIRECTORY)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # Initializes the WebDriver for Firefox.
    driver = webdriver.Firefox(options=options)

    return driver


def ensure_download_directory(path: str) -> None:
    """
    Ensures that the download directory exists.

    Args:
        path (str): The path to the download directory.
    """

    # Creates the download directory if it does not exist.
    Path(path).mkdir(parents=True, exist_ok=True)
