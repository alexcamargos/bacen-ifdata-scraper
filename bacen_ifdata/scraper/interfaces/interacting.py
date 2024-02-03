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


from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        ElementClickInterceptedException,
                                        MoveTargetOutOfBoundsException)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bacen_ifdata.utilities import config


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
            ElementClickInterceptedException: If the element is intercepted by another element.
            MoveTargetOutOfBoundsException: If the element is outside the boundaries of the window.
        """

        try:
            # Wait until the element is clickable.
            element = WebDriverWait(self._driver, wait_time).until(
                EC.element_to_be_clickable((by_method, locator))
            )
            # Click the element using JavaScript.
            self._driver.execute_script('arguments[0].click();', element)

        except TimeoutException:
            print(f"Timeout: O elemento {
                locator} não se tornou clicável após {wait_time} segundos.")
            raise
        except NoSuchElementException:
            print(f"Não encontrado: O elemento {
                locator} não foi encontrado na página.")
            raise
        except ElementClickInterceptedException:
            print(f'Elemento interceptado: O elemento {
                locator} foi interceptado por outro elemento.')
            raise
        except MoveTargetOutOfBoundsException:
            print(f'Fora dos limites: O elemento {
                locator} está fora dos limites da janela.')
            raise

    def initialize(self, url: str) -> None:
        """Initializes a WebDriver session with Firefox."""

        self._driver.get(url)

    def ensure_dropdown_content(self, dropdown_id: str, wait_time: int):
        """Selects an option from a dropdown menu on a web page."""

        self.__ensure_clickable(wait_time, By.ID, dropdown_id)

    def select_dropdown_option(self, option_text: str, wait_time: int):
        """Selects an option from a dropdown menu on a web page."""

        option_xpath = f"//a[normalize-space(text())='{option_text}']"
        self.__ensure_clickable(wait_time, By.XPATH, option_xpath)

    def get_dropdown_options(self, dropdown_id: str) -> list:
        """Returns a list of options from a dropdown menu on a web page."""

        self.ensure_dropdown_content('btnDataBase', config.TIMEOUT)

        # Using __ensure_clickable() not working here.
        # Need to investigate further.
        # Solution is to use WebDriverWait() directly.
        WebDriverWait(self._driver, config.TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="ulDataBase"]/li[1]/a')
                                       )
        )

        dropdown = self._driver.find_element(By.ID, dropdown_id)
        dropdown_items = dropdown.find_elements(By.TAG_NAME, 'li')

        dropdown_texts = [
            item.find_element(By.TAG_NAME, 'a').text for item in dropdown_items
            if item.text.strip() != ''
        ]

        self.select_dropdown_option(dropdown_texts[0], config.TIMEOUT)

        return dropdown_texts

    def download_report(self, wait_time: int):
        """Downloads a report from a web page."""

        # Wait for the dataTable element to be visible.
        try:
            WebDriverWait(self._driver, wait_time).until(
                EC.visibility_of_element_located((By.ID, 'dataTable')))
        except TimeoutException:
            print(f"Timeout: O elemento dataTable não se tornou visível após {
                  wait_time} segundos.")
            raise

        # Click the "Exportar CSV" button.
        self.__ensure_clickable(wait_time, By.ID, 'aExportCsv')
