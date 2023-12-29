#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: run.py
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

from bacen_ifdata_scraper.utils import initialize_webdriver
from bacen_ifdata_scraper.scraper import download_ifdata_reports
import bacen_ifdata_scraper.config as config

if __name__ == '__main__':
    driver = initialize_webdriver()
    download_ifdata_reports(driver, config.LAST_BASE_DATE, config.INSTITUTION_TYPE, config.REPORT_TYPE)
