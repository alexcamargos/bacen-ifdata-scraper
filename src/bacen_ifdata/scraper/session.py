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
from typing import TypedDict

from loguru import logger

from bacen_ifdata.scraper.interfaces import BrowserProtocol
from bacen_ifdata.utilities.configurations import Config as Cfg
from bacen_ifdata.utilities.humanize import seconds_to_human_readable


class SessionData(TypedDict):
    """TypedDict for session data.

    Attributes:
        url (str): The URL of the session.
        is_headless (bool): Indicates if the browser is in headless mode.
        duration (float): The duration of the session in seconds.
        reports_downloaded (int): The number of reports downloaded during the session.
    """

    url: str
    is_headless: bool
    duration: float
    reports_downloaded: int


class Session:
    """
    Manages a web session for interacting with the IF.data tool.

    Attributes:
        _url (str): The URL to open in the web session.
        _browser (Browser): A browser interface for web interactions.
        session_data (SessionData): Data about the session,
                             such as duration and number of reports downloaded.
        _started (float): The start time of the session.

    Methods:
        _ensure_and_select_dropdown_option(element_id, option): Ensures the dropdown menu is clickable
                                                                and selects the desired option.
        open(): Opens the URL in a web browser.
        cleanup(): Cleans up the web session and log details.
        get_data_bases(): Returns a list of available data bases.
        download_reports(data_base, institution_type, report_type): Downloads reports from the IF.data tool.
    """

    def __init__(self, browser: BrowserProtocol, url: str) -> None:
        """Initializes a new instance of the Session class.

        Args:
            browser (BrowserProtocol): The browser instance for web interactions.
            url (str): The URL to open in the web session.
        """

        self._browser = browser
        self._url = url

        self.session_data: SessionData = {
            'url': self._url,
            'is_headless': self._browser.is_headless,
            'duration': 0,
            'reports_downloaded': 0,
        }

        self._started = time()

    def _ensure_and_select_dropdown_option(self, element_id: str, option: str) -> None:
        """Ensures the dropdown menu is clickable and selects the desired option.

        Args:
            element_id (str): The ID of the dropdown menu element.
            option (str): The option to select in the dropdown menu.
        """

        # Ensuring the dropdown menu is clickable.
        self._browser.ensure_dropdown_content(element_id, Cfg.TIMEOUT)
        # Selecting the desired option in the "ulDataBase" dropdown menu.
        self._browser.select_dropdown_option(option, Cfg.TIMEOUT)

    def open(self) -> None:
        """Opens the URL in a web browser."""

        self._browser.initialize(self._url)

    def cleanup(self) -> None:
        """Cleans up the web session and log details."""

        # Calculate the session duration and log details.
        session_finished = time()
        self.session_data['duration'] = session_finished - self._started
        human_readable_duration = seconds_to_human_readable(self.session_data['duration'])

        logger.info(f"Headless mode: {self.session_data['is_headless']}.")
        logger.info(
            f"Session duration: {human_readable_duration.hours}h {human_readable_duration.minutes}m {human_readable_duration.seconds}s."
        )
        logger.info(f"Reports downloaded: {self.session_data['reports_downloaded']}.")

        self._browser.quit()

    def get_data_bases(self) -> list[str]:
        """Returns a list of available data bases.

        Returns:
            list[str]: A list of available data bases.
        """

        return self._browser.get_dropdown_options('ulDataBase')

    def download_reports(self, data_base: str, institution_type: str, report_type: str) -> None:
        """Downloads reports from the IF.data tool.

        IMPORTANT: The system generates reports dynamically, so we need to
        ensure the page content is loaded before proceeding.

        Args:
            data_base (str): The base date for the reports to be downloaded.
            institution_type (str): The institution type for the reports to be downloaded.
            report_type (str): The report type to be downloaded.
        """

        # Selecting the desired option in the "ulDataBase" dropdown menu.
        self._ensure_and_select_dropdown_option('btnDataBase', data_base)

        # Selecting the desired option in the "ulTipoInst" dropdown menu.
        self._ensure_and_select_dropdown_option('btnTipoInst', institution_type)

        # Selecting the desired option in the "ulRelatorio" dropdown menu.
        self._ensure_and_select_dropdown_option('btnRelatorio', report_type)

        # Ensure the report content is loaded before proceeding with the download of the CSV file.
        self._browser.download_report(Cfg.TIMEOUT)

        # Update the counter for downloaded reports.
        self.session_data['reports_downloaded'] += 1
