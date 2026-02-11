#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: interacting.py
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
Interface definitions for Bacen IF.data AutoScraper & Data Manager

This module defines the Browser class, which provides methods for interacting
with a web browser, including clicking elements, navigating, and downloading reports.

Author: Alexsander Lopes Camargos
License: MIT
"""

from time import sleep

from loguru import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bacen_ifdata.scraper.utils import ensure_clickable
from bacen_ifdata.utilities.configurations import Config as Cfg


class Browser:
    """A class for interacting with a web browser using Selenium WebDriver."""

    def __init__(self, driver: WebDriver) -> None:
        """Initializes a new instance of the Browser class with the given WebDriver.

        Args:
            driver (WebDriver): The WebDriver instance for browser interactions.
        """

        self._driver = driver

    def _ensure_clickable(self, wait_time: int, by_method: By, locator: str) -> None:
        """Waits for an element to be clickable on a web page and then clicks it.

        This is a wrapper around the ensure_clickable utility function.

        Args:
            wait_time (int): The maximum time to wait for the element to become clickable.
            by_method (By): The Selenium By method to locate the element.
            locator (str): The locator string for finding the element.

        Raises:
            TimeoutException: If the element doesn't become clickable after wait_time seconds.
            NoSuchElementException: If the element is not found on the page.
            ElementClickInterceptedException: If the element is intercepted by another element.
            MoveTargetOutOfBoundsException: If the element is outside the boundaries of the window.
        """

        ensure_clickable(self._driver, wait_time, by_method, locator)

    def initialize(self, url: str) -> None:
        """Initializes a WebDriver session with Firefox and opens the specified URL.

        Args:
            url (str): The URL to open in the web browser.
        """

        self._driver.get(url)

    def quit(self) -> None:
        """Quits the WebDriver session."""

        self._driver.quit()

    @property
    def is_headless(self) -> bool:
        """Returns True if the browser is running in headless mode."""

        return self._driver.capabilities['moz:headless']

    def ensure_dropdown_content(self, dropdown_id: str, wait_time: int) -> None:
        """Selects an option from a dropdown menu on a web page.

        Args:
            dropdown_id (str): The ID of the dropdown menu element.
            wait_time (int): The maximum time to wait for the dropdown to become clickable.
        """

        self._ensure_clickable(wait_time, By.ID, dropdown_id)

    def select_dropdown_option(self, option_text: str, wait_time: int) -> None:
        """Selects an option from a dropdown menu on a web page.

        Args:
            option_text (str): The text of the option to select.
            wait_time (int): The maximum time to wait for the option to become clickable.
        """

        option_xpath = f"//a[normalize-space(text())='{option_text}']"
        self._ensure_clickable(wait_time, By.XPATH, option_xpath)

    def get_dropdown_options(self, dropdown_id: str) -> list[str]:
        """Returns a list of options from a dropdown menu on a web page.

        Args:
            dropdown_id (str): The ID of the dropdown menu element.

        Returns:
            list[str]: A list of option texts from the dropdown menu.
        """

        self.ensure_dropdown_content('btnDataBase', Cfg.TIMEOUT)

        # NOTE: Using _ensure_clickable() not working here.
        # Need to investigate further.
        # Solution is to use WebDriverWait() directly.
        WebDriverWait(self._driver, Cfg.TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ulDataBase"]/li[1]/a'))
        )

        dropdown = self._driver.find_element(By.ID, dropdown_id)
        dropdown_items = dropdown.find_elements(By.TAG_NAME, 'li')

        dropdown_texts = [
            item.find_element(By.TAG_NAME, 'a').text for item in dropdown_items if item.text.strip() != ''
        ]

        self.select_dropdown_option(dropdown_texts[0], Cfg.TIMEOUT)

        return dropdown_texts

    def download_report(self, wait_time: int) -> None:
        """Downloads a report from a web page by clicking the "Exportar CSV" button.

        Args:
            wait_time (int): The maximum time to wait for the button to become clickable.
        """

        # Wait for the dataTable element to be visible.
        try:
            WebDriverWait(self._driver, wait_time).until(EC.visibility_of_element_located((By.ID, 'dataTable')))
        except TimeoutException:
            logger.exception(f'Timeout: O elemento dataTable não se tornou visível após {wait_time} segundos.')
            raise

        # BUG: This workaround ensures that the Blob object is fully initialized
        # before the button is clicked. For a detailed description of the
        # underlying issue, please refer to the BUG comment in `scraping.py`.
        sleep(3)

        # Click the "Exportar CSV" button.
        self._ensure_clickable(wait_time, By.ID, 'aExportCsv')
