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
import os
import time

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from bacen_ifdata_scraper.config import DOWNLOAD_DIRECTORY
from bacen_ifdata_scraper.institutions_type import InstitutionType as INSTITUTIONS
from bacen_ifdata_scraper.reports_type import REPORTS


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
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # Initializes the WebDriver for Firefox.
    driver = webdriver.Firefox(options=options)

    return driver


def build_directory_path(base_dir, *parts):
    """
    Constructs a safe and absolute directory path from provided components.

    This function takes multiple arguments (parts) that are joined together
    to form a complete and absolute directory path, resolves the final path
    to ensure it is absolute and removes any relative or redundant references.

    Parameters:
        base_dir (str): The base directory where the path will be created.
        *parts (str): Variable components of the directory path.
                      Each argument is a part of the final path,
                      such as the name of a subdirectory or file.

    Returns:
        Path: A Path object representing the absolute and resolved path.

    Example:
    >>> build_directory_path('folder1', 'subfolder2')
    PosixPath('/path/to/DOWNLOAD_DIRECTORY/folder1/subfolder2')
    """

    return Path(base_dir, *parts).resolve()


def ensure_directory(path: Path) -> None:
    """
    Ensures that the directory exists.

    Args:
        path (str): The path to the directory.
    """

    # Creates the directory if it does not exist.
    path.mkdir(parents=True, exist_ok=True)


def wait_for_download_completion(directory: str, filename: str, timeout: int = 300) -> bool:
    """
    Waits until a file has been completely downloaded.

    This function checks the specified download directory for the presence of a
    fully downloaded file. It waits until the file with the specified beginning
    of the filename is present and no longer has a temporary '.part' or other
    browser-specific temporary extension.

    Args:
        directory (str): The directory where the file is being downloaded.
        filename (str): The beginning of the filename to check for.
        timeout (int): The maximum amount of time to wait for the file to download, in seconds.
                       Defaults to 300 seconds.

    Returns:
        bool: True if the file was downloaded completely within
              the timeout, False otherwise.
    """

    start_time = time.time()

    while True:
        # Check if the file exists.
        for fname in os.listdir(directory):
            if fname.startswith(filename) \
                and not fname.endswith('.crdownload') \
                    and not fname.endswith('.part'):
                return True

        if time.time() - start_time > timeout:
            return False

        time.sleep(1)


def check_file_already_downloaded(file: Path) -> bool:
    """
    Checks if the file has already been downloaded.

    Args:
        file (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """

    return Path(file).exists()


def validate_report_selection(institution: str, report: str, data_base: list) -> list:
    """Validates the report selection."""

    if institution == INSTITUTIONS.PRUDENTIAL_CONGLOMERATES and \
            report == REPORTS[INSTITUTIONS.PRUDENTIAL_CONGLOMERATES].SEGMENTATION:
        cut_off_date = '03/2017'
    elif institution == INSTITUTIONS.PRUDENTIAL_CONGLOMERATES and \
            report == REPORTS[INSTITUTIONS.PRUDENTIAL_CONGLOMERATES].CAPITAL_INFORMATION:
        cut_off_date = '03/2015'
    elif institution == INSTITUTIONS.PRUDENTIAL_CONGLOMERATES:
        cut_off_date = '03/2014'
    elif institution == INSTITUTIONS.FOREIGN_EXCHANGE:
        cut_off_date = '12/2014'
    else:
        # No cut-off for other institutions and reports.
        return data_base

    try:
        data_base_index = data_base.index(cut_off_date)
        return data_base[:data_base_index + 1]
    except ValueError:
        # cut_off_date not in data_base, return as is
        return data_base
