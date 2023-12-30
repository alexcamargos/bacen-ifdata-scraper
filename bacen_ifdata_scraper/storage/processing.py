#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: processing.py
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

from os import path
from time import sleep

import shutil

import bacen_ifdata_scraper.config as config


def process_downloaded_files(src: str, dst: str) -> None:
    """Process downloaded files."""

    sleep(3)

    if path.exists(f'{config.DOWNLOAD_DIRECTORY}\\{src}'):
        # Rename the downloaded file.
        shutil.move(f'{config.DOWNLOAD_DIRECTORY}\\{src}',
                    f'{config.DOWNLOAD_DIRECTORY}\\{dst}')

        print(f'File {src} moved to {config.DOWNLOAD_DIRECTORY}\\{dst}.')
