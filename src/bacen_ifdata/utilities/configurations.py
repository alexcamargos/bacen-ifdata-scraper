#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: configurations.py
#  Version: 0.0.3
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
Configuration settings for Bacen IF.data AutoScraper & Data Manager

This module contains the configuration settings for scraping IF.data reports from
Banco Central do Brasil, including URLs, timeouts, and specific report details.

Author: Alexsander Lopes Camargos
License: MIT
"""

from enum import Enum
from pathlib import Path


class Config(Enum):
    """Configuration settings for Bacen IF.data AutoScraper & Data Manager."""

    # URL of the page where the reports are located.
    URL = 'https://www3.bcb.gov.br/ifdata/index2024.html'
    # Maximum waiting time for elements to load.
    TIMEOUT = 120
    BASE_DIRECTORY = Path.cwd()
    DOWNLOAD_DIRECTORY = BASE_DIRECTORY / 'data' / 'raw'
    DOWNLOAD_FILE_NAME = 'dados.csv'
    PROCESSED_FILES_DIRECTORY = BASE_DIRECTORY / 'data' / 'processed'
    TRANSFORMED_FILES_DIRECTORY = BASE_DIRECTORY / 'data' / 'transformed'


__all__ = ['Config']
