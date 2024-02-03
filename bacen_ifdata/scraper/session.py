#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: session.py
#  Version: 0.0.2
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
Session management for Bacen IF.data AutoScraper & Data Manager

This module defines the Session class which manages web interactions and report downloads
from the IF.data tool of Banco Central do Brasil.

Author: Alexsander Lopes Camargos
License: MIT
"""

from time import time

from selenium.webdriver.firefox.webdriver import WebDriver

from bacen_ifdata.utilities import config
from bacen_ifdata.scraper.interfaces.interacting import Browser
from bacen_ifdata.utilities.humanize import seconds_to_human_readable


class Session:
    """
    Manages a web session for interacting with the IF.data tool.

    Attributes:
        _driver (WebDriver): The WebDriver instance for browser interactions.
        _url (str): The URL to open in the web session.
        browser (Browser): A browser interface for web interactions.
        session_data (dict): Data about the session,
                             such as duration and number of reports downloaded.
        _started (float): The start time of the session.
    """

    def __init__(self, driver: WebDriver, url: str) -> None:
        """Initializes a new instance of the Session class."""

        self._driver = driver
        self._url = url
        self.browser = Browser(self._driver)

        self.session_data = {'url': self._url,
                             'is_headless': self._driver.capabilities['moz:headless'],
                             'duration': 0,
                             'reports_downloaded': 0
                             }

        self._started = time()

    def __ensure_and_select_dropdown_option(self, element_id: str, option: str) -> None:
        """Ensures the dropdown menu is clickable and selects the desired option."""

        # Ensuring the dropdown menu is clickable.
        self.browser.ensure_dropdown_content(element_id, config.TIMEOUT)
        # Selecting the desired option in the "ulDataBase" dropdown menu.
        self.browser.select_dropdown_option(option, config.TIMEOUT)

    def open(self) -> None:
        """Opens the URL in a web browser."""

        self.browser.initialize(self._url)

    def cleanup(self) -> None:
        """Cleans up the web session and prints details."""

        # Calculate the session duration and print details.
        finished = time()
        self.session_data['duration'] = finished - self._started
        hours, minutes, seconds = seconds_to_human_readable(self.session_data['duration'])

        print(f"Headless mode: {self.session_data['is_headless']}.")
        print(f"Session duration: {hours}h {minutes}m {seconds}s.")
        print(f"Reports downloaded: {
              self.session_data['reports_downloaded']}.")

        self._driver.quit()

    def get_data_bases(self) -> list:
        """Returns a list of available data bases."""

        return self.browser.get_dropdown_options('ulDataBase')

    def download_reports(self,
                         data_base: str,
                         institution_type: str,
                         report_type: str) -> None:
        """
        Downloads reports from the IF.data tool.

        IMPORTANT: The system generates reports dynamically, so we need to
        ensure the page content is loaded before proceeding.
        """

        # Selecting the desired option in the "ulDataBase" dropdown menu.
        self.__ensure_and_select_dropdown_option('btnDataBase',
                                                 data_base)

        # Selecting the desired option in the "ulTipoInst" dropdown menu.
        self.__ensure_and_select_dropdown_option('btnTipoInst',
                                                 institution_type)

        # Selecting the desired option in the "ulRelatorio" dropdown menu.
        self.__ensure_and_select_dropdown_option('btnRelatorio',
                                                 report_type)

        # Ensure the report content is loaded before proceeding with
        # the download of the CSV file.
        self.browser.download_report(config.TIMEOUT)

        # Update the counter for downloaded reports.
        self.session_data['reports_downloaded'] += 1
