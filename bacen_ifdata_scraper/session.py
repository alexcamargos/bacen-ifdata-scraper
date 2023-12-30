#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: session.py
#  Version: 0.0.2
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

from time import time

from selenium.webdriver.firefox.webdriver import WebDriver

from bacen_ifdata_scraper import config
from bacen_ifdata_scraper.interfaces import Browser


class Session:

    def __init__(self, driver: WebDriver, url: str) -> None:
        """Initializes a new instance of the Session class."""

        self._driver = driver
        self.browser = Browser(self._driver)
        self._url = url

        self.session_data = {'url': self._url,
                             'is_headless': self._driver.capabilities['moz:headless'],
                             'duration': 0,
                             'reports_downloaded': 0
                             }

        self._started = time()

    def open(self):
        self.browser.initialize(self._url)

    def cleanup(self):
        finished = time()
        self.session_data['duration'] = finished - self._started

        print(f"Headless mode: {self.session_data['is_headless']}.")
        print(f"Session duration: {self.session_data['duration']} seconds.")
        print(f"Reports downloaded: {
              self.session_data['reports_downloaded']}.")

        self._driver.quit()

    def download_reports(self,
                         data_base: str,
                         institution_type: str,
                         report_type: str):
        # IMPORTANTE: O sistema gera os relatórios de forma dinâmica, então precisamos
        # garantir que o conteúdo da página esteja carregado antes de prosseguir.
        # Para isso, vamos usar a função ensure_clickable() para garantir que o conteúdo
        # esteja carregado antes de prosseguirmos.

        # Selecionando a opção desejada no menu dropdown "ulDataBase".
        self.browser.ensure_dropdown_content('btnDataBase', config.TIMEOUT)
        self.browser.select_dropdown_option(data_base, config.TIMEOUT)

        # Selecionando a opção desejada no menu dropdown "ulTipoInst".
        self.browser.ensure_dropdown_content('btnTipoInst', config.TIMEOUT)
        self.browser.select_dropdown_option(institution_type, config.TIMEOUT)

        # Selecionando a opção desejada no menu dropdown "ulRelatorio".
        self.browser.ensure_dropdown_content('btnRelatorio', config.TIMEOUT)
        self.browser.select_dropdown_option(report_type, config.TIMEOUT)

        # Garanta que o conteúdo do relatório esteja carregado antes de
        # prosseguir com o download do arquivo CSV.
        self.browser.download_report(config.TIMEOUT)

        # Atualize o contador de relatórios baixados.
        self.session_data['reports_downloaded'] += 1
