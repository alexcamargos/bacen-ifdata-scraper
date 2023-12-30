#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: interfaces.py
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
Interface definitions for Banco Central do Brasil IF.data Scraper

This module defines the Browser class, which provides methods for interacting
with a web browser, including clicking elements, navigating, and downloading reports.

Author: Alexsander Lopes Camargos
License: MIT
"""


from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Browser:
    """A class for interacting with a web browser.

    Attributes:
        _driver (WebDriver): The WebDriver instance for browser interactions.
    """

    def __init__(self, driver: WebDriver) -> None:
        """Initializes a new instance of the Browser class."""

        self._driver = driver

    def __ensure_clickable(self,
                           wait_time: int,
                           by_method: str,
                           locator: str) -> None:
        """
        Waits for an element to be clickable on a web page and then clicks it.

        Args:
            wait_time (int): The maximum time to wait for the element to become clickable.
            by_method (str): The Selenium By method to locate the element.
            locator (str): The locator string for finding the element.

        Raises:
            TimeoutException: If the element doesn't become clickable after wait_time seconds.
            NoSuchElementException: If the element is not found on the page.
        """

        try:
            element = WebDriverWait(self._driver, wait_time).until(
                EC.element_to_be_clickable((by_method, locator))
            )
            element.click()
        except TimeoutException:
            print(f"Timeout: O elemento {
                locator} não se tornou clicável após {wait_time} segundos.")
            raise
        except NoSuchElementException:
            print(f"Não encontrado: O elemento {
                locator} não foi encontrado na página.")
            raise

    def initialize(self, url: str) -> None:
        """Initializes a WebDriver session with Firefox."""

        self._driver.get(url)

    def ensure_dropdown_content(self, dropdown_id: str, wait_time: int):
        """Selects an option from a dropdown menu on a web page."""

        self.__ensure_clickable(wait_time, By.ID, dropdown_id)

    def select_dropdown_option(self, option_text: str, wait_time: int):
        """Selects an option from a dropdown menu on a web page."""

        option_xpath = f"//a[text()='{option_text}']"
        self.__ensure_clickable(wait_time, By.XPATH, option_xpath)

    def download_report(self, wait_time: int):
        """Downloads a report from a web page."""

        self.__ensure_clickable(wait_time, By.ID, 'aExportCsv')
