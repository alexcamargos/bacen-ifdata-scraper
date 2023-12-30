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
from selenium.webdriver.firefox.webdriver import WebDriver


def initialize_webdriver() -> WebDriver:
    """
    Initializes a WebDriver session with Firefox.

    Returns:
    - driver (webdriver): The WebDriver instance being used to interact with the web page.
    """

    # Inicializa o WebDriver para o Firefox.
    driver = webdriver.Firefox()

    return driver
