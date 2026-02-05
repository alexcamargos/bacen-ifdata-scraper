#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: financial_conglomerates.py
#  Version: 0.0.1
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

from bacen_ifdata.data_transformer.transformers.base import BaseTransformer


# pylint: disable=too-few-public-methods
class FinancialConglomeratesTransformer(BaseTransformer):
    """Converts raw input data into well-organized, structured information
    tailored for financial conglomerates.
    """

    def apply_business_rules(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Applies specific business rules to the DataFrame.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be processed.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """

        # Capitalizes the city name
        if 'cidade' in data_frame.columns:
            data_frame['cidade'] = data_frame['cidade'].str.title()

        # Fills null values in the segment column
        if 'segmento' in data_frame.columns:
            data_frame['segmento'] = data_frame['segmento'].fillna('Não informado')

        return data_frame
