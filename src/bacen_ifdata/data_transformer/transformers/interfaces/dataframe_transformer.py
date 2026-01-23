#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: dataframe_transformer.py
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

from typing import Protocol
from typing import List

import pandas as pd


class DataFrameTransformerProtocol(Protocol):
    """Defines a standard interface for classes that transform pandas DataFrames."""

    def apply_business_rules(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("You should implement this method.")

    def transform_numeric_columns(self, data_frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        raise NotImplementedError("You should implement this method.")

    def transform_percentage_columns(self, data_frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        raise NotImplementedError("You should implement this method.")

    def transform_date_columns(self, data_frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        raise NotImplementedError("You should implement this method.")

    def transform_categorical_columns(self, data_frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        raise NotImplementedError("You should implement this method.")

    def transform_text_columns(self, data_frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        raise NotImplementedError("You should implement this method.")
