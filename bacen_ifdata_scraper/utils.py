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

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def ensure_clickable(driver: webdriver, wait_time: int, by_method: str, locator: str):
    """
    Waits for an element to be clickable on a web page and then clicks it.

    This function uses explicit wait to pause the execution until the specified
    element is determined to be clickable. Once clickable, the function
    performs a click action on the element.

    Parameters:
    - driver (webdriver): The WebDriver instance being used to interact with the web page.
    - wait_time (int): The maximum number of seconds to wait for the element to become clickable.
    - by_method (str): The method used to locate the element (e.g., By.ID, By.XPATH).
    - locator (str): The locator string used with the by_method to find the element.

    Raises:
    - TimeoutException: If the element is not clickable within the specified wait_time.

    Returns:
    None
    """

    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((by_method, locator))
        )
        element.click()
    except TimeoutException:
        print(f"Timeout: O elemento {
              locator} não se tornou clicável após {wait_time} segundos.")
    except NoSuchElementException:
        print(f"Não encontrado: O elemento {
              locator} não foi encontrado na página.")
