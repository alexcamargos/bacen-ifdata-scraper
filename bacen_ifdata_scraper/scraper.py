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

from bacen_ifdata_scraper import config
from bacen_ifdata_scraper.utils import ensure_clickable


def download_ifdata_reports(driver: webdriver,
                            data_base: str,
                            institution_type: str,
                            report_type: str):
    """
    Initializes a WebDriver session with Firefox, navigates to a specific URL,
    and interacts with a dynamic web page to ensure that specific elements
    are clickable before proceeding.
    """

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
                     f"//a[text()='{data_base}']")

    # Forçando o inicio do carregando do conteúdo do dropdown menu "ulTipoInst".
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'btnTipoInst')

    # Garanta que o conteúdo do dropdown menu "ulTipoInst" esteja carregado antes de prosseguir.
    ensure_clickable(driver,
                     config.TIMEOUT,
                     By.XPATH,
                     f"//a[text()='{institution_type}']")

    # Forçando o inicio do carregando do conteúdo do dropdown menu "ulRelatorio".
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'btnRelatorio')

    # Garanta que o conteúdo do dropdown menu "ulRelatorio" esteja carregado antes de prosseguir.
    ensure_clickable(driver,
                     config.TIMEOUT,
                     By.XPATH,
                     f"//a[text()='{report_type}']")

    # Garanta que o conteúdo do relatório esteja carregado antes de
    # prosseguir com o download do arquivo CSV.
    # TODO: Implementar checagem de termino do download.
    ensure_clickable(driver, config.TIMEOUT, By.ID, 'aExportCsv')
