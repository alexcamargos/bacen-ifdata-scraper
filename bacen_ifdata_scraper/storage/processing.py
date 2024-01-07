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

from time import sleep
from pathlib import Path


def process_downloaded_files(src: Path, dst: Path) -> None:
    """
    Check if the downloaded files are complete and move
    them to the destination folder.
    """

    # Wait for the download to complete.
    # sleep(3)

    # Check if the file exists.
    if src.exists():
        # Move the file to the destination folder.
        src.rename(dst)
    else:
        raise FileNotFoundError(f'File {src} does not exist.')
