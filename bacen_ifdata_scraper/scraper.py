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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL da página onde estão os relatórios.
URL = 'https://www3.bcb.gov.br/ifdata/'
TIMEOUT = 120  # Tempo máximo de espera para carregamento de elementos.
LAST_BASE_DATE = '06/2023'  # Data-base do último relatório disponível.
# Tipo de instituição.
INSTITUTION_TYPE = 'Conglomerados Financeiros e Instituições Independentes'
REPORT_TYPE = 'Ativo'  # Tipo de relatório.


def ensure_clickable(driver: webdriver, wait_time: int, by_method: str, locator: str):
    """
    Waits for an element to be clickable on a web page and then clicks it.

    This function uses explicit wait to pause the execution until the specified element is determined to be clickable. Once clickable, the function performs a click action on the element.

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

    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((by_method, locator))
    )
    element.click()


# Inicializa o WebDriver para o Firefox.
driver = webdriver.Firefox()

# Acesse a página onde estão os relatórios.
driver.get(URL)

# O sistema gera os relatórios de forma dinâmica, então precisamos garantir que
# o conteúdo da página esteja carregado antes de prosseguir. Para isso, vamos
# usar a função ensure_clickable() para garantir que o conteúdo esteja carregado
# antes de prosseguirmos.

# Forçando o inicio do carregando do conteúdo do dropdown menu "ulDataBase".
btn_data_base = driver.find_element(By.ID, 'btnDataBase')
btn_data_base.click()

# Garanta que o conteúdo do dropdown menu "ulDataBase" esteja carregado antes de prosseguir.
ensure_clickable(driver,
                 TIMEOUT,
                 By.XPATH,
                 f"//a[text()='{LAST_BASE_DATE}']")

# Forçando o inicio do carregando do conteúdo do dropdown menu "ulTipoInst".
btn_tipo_iInst = driver.find_element(By.ID, 'btnTipoInst')
btn_tipo_iInst.click()

# Garanta que o conteúdo do dropdown menu "ulTipoInst" esteja carregado antes de prosseguir.
ensure_clickable(driver,
                 TIMEOUT,
                 By.XPATH,
                 f"//a[text()='{INSTITUTION_TYPE}']")

# Forçando o inicio do carregando do conteúdo do dropdown menu "ulRelatorio".
btn_relatorio = driver.find_element(By.ID, 'btnRelatorio')
btn_relatorio.click()

# Garanta que o conteúdo do dropdown menu "ulRelatorio" esteja carregado antes de prosseguir.
ensure_clickable(driver,
                 TIMEOUT,
                 By.XPATH,
                 f"//a[text()='{REPORT_TYPE}']")

# Garanta que o conteúdo do relatório esteja carregado antes de
# prosseguir com o download do arquivo CSV.
ensure_clickable(driver, TIMEOUT, By.ID, 'aExportCsv')

# TODO: Implementar checagem de termino do download.

# Feche o navegador após o download (opcional).
# driver.quit()
