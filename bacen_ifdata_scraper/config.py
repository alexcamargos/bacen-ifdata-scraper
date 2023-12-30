#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: config.py
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
Configuration settings for Banco Central do Brasil IF.data Scraper

This module contains the configuration settings for scraping IF.data reports from
Banco Central do Brasil, including URLs, timeouts, and specific report details.

Author: Alexsander Lopes Camargos
License: MIT
"""

# URL of the page where the reports are located.
URL = 'https://www3.bcb.gov.br/ifdata/'

# Maximum waiting time for elements to load.
TIMEOUT = 120

# Base date of the last available report.
LAST_BASE_DATE = '06/2023'

# Type of institution for the report.
INSTITUTION_TYPE = 'Conglomerados Financeiros e Instituições Independentes'

# Type of report to download.
REPORT_TYPE = 'Ativo'
