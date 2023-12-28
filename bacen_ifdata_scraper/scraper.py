#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: scraper.py
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
Este sistema foi projetado para automatizar o download dos relatórios da ferramenta
IF.data do Banco Central do Brasil. Criado para facilitar a integração com ferramentas
automatizadas de análise e visualização de dados, garantido acesso fácil e oportuno aos dados.
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


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


def main():
    """
    Initializes a WebDriver session with Firefox, navigates to a specific URL,
    and interacts with a dynamic web page to ensure that specific elements
    are clickable before proceeding.
    """

    # Inicializa o WebDriver para o Firefox.
    driver = webdriver.Firefox()

    # Acesse a página onde estão os relatórios.
    driver.get(config.URL)

    # O sistema gera os relatórios de forma dinâmica, então precisamos garantir que
    # o conteúdo da página esteja carregado antes de prosseguir. Para isso, vamos
    # usar a função ensure_clickable() para garantir que o conteúdo esteja carregado
    # antes de prosseguirmos.

    # Forçando o inicio do carregando do conteúdo do dropdown menu "ulDataBase".
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'btnDataBase')

    # Garanta que o conteúdo do dropdown menu "ulDataBase" esteja carregado antes de prosseguir.
    ensure_clickable(driver,
                     config.TIMEOUT,
                     By.XPATH,
                     f"//a[text()='{config.LAST_BASE_DATE}']")

    # Forçando o inicio do carregando do conteúdo do dropdown menu "ulTipoInst".
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'btnTipoInst')

    # Garanta que o conteúdo do dropdown menu "ulTipoInst" esteja carregado antes de prosseguir.
    ensure_clickable(driver,
                     config.TIMEOUT,
                     By.XPATH,
                     f"//a[text()='{config.INSTITUTION_TYPE}']")

    # Forçando o inicio do carregando do conteúdo do dropdown menu "ulRelatorio".
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'btnRelatorio')

    # Garanta que o conteúdo do dropdown menu "ulRelatorio" esteja carregado antes de prosseguir.
    ensure_clickable(driver,
                     config.TIMEOUT,
                     By.XPATH,
                     f"//a[text()='{config.REPORT_TYPE}']")

    # Garanta que o conteúdo do relatório esteja carregado antes de
    # prosseguir com o download do arquivo CSV.
    # TODO: Implementar checagem de termino do download.
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'aExportCsv')


if __name__ == '__main__':
    main()
