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
Banco Central do Brasil IF.data Scraper

This script is designed to automate the download of reports from the Banco Central do Brasil's
IF.data tool. It facilitates the integration with automated data analysis and visualization tools,
ensuring easy and timely access to data.

Author: Alexsander Lopes Camargos
License: MIT
"""

from bacen_ifdata_scraper.config import *
from bacen_ifdata_scraper.session import Session
from bacen_ifdata_scraper.utils import initialize_webdriver

if __name__ == '__main__':
    driver = initialize_webdriver()
    session = Session(driver, URL)

    session.open()
    data_base = session.get_data_bases()
    session.download_reports(data_base[0],
                             InstitutionType.FINANCIAL_CONGLOMERATES,
                             REPORTS[InstitutionType.FINANCIAL_CONGLOMERATES].PORTFOLIO_NUMBER_CLIENTS_OPERATIONS,
                             )
    session.cleanup()
