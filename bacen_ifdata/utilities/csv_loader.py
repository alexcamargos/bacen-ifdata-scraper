#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: csv_loader.py
#  Version: 0.0.2
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
Bacen IF.data AutoScraper & Data Manager

This script is designed to automate the download of reports from the Banco Central do Brasil's
IF.data tool. It facilitates the integration with automated data analysis and visualization tools,
ensuring easy and timely access to data.

Author: Alexsander Lopes Camargos
License: MIT
"""

import pandas as pd


def load_csv_data(file_path: str, options: dict) -> pd.DataFrame:
    """Loads data from a CSV file.

    This function loads data from a CSV file and returns it as a pandas DataFrame.

    Arguments:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The data loaded from the CSV file.
    """

    if not options:
        options = {
            'sep': ";"
        }

    # Load the data.
    return pd.read_csv(file_path, **options)
