#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: prudential_conglomerates.py
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

from typing import List

import pandas as pd


# pylint: disable=missing-class-docstring, missing-function-docstring
class PrudentialConglomeratesTransformer:
    """Converts raw input data into well-organized, structured information
    tailored for prudential conglomerates.
    """

    def __normalize_percentage_series(self, series: pd.Series) -> pd.Series:
        """Removes the '%' sign from a pandas Series and converts it to float."""

        series_cleaned = series.str.replace('%', '', regex=False) \
                               .str.replace(',', '.', regex=False)

        return pd.to_numeric(series_cleaned, errors='coerce') / 100

    def __normalize_numeric_series(self, series: pd.Series) -> pd.Series:
        """Cleans and converts a pandas Series to a numeric type, handling errors gracefully."""

        # If the series contains decimal values, normalize them.
        series_cleaned = series.str.replace('.', '', regex=False) \
                               .str.replace(',', '.', regex=False)

        # Convert the cleaned series to numeric, rounding and converting to Int64.
        numeric_series = pd.to_numeric(series_cleaned, errors='coerce')

        return numeric_series.round().astype('Int64')

    def apply_business_rules(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Applies specific business rules to the DataFrame."""

        # Capitalizes the city name
        if 'cidade' in data_frame.columns:
            data_frame['cidade'] = data_frame['cidade'].str.title()

        # Fills null values in the segment column
        if 'segmento' in data_frame.columns:
            data_frame['segmento'] = data_frame['segmento'].fillna('Não informado')

        return data_frame

    def transform_numeric_columns(self, data_frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Transforms numeric columns in the DataFrame to a standard numeric format."""

        for column in columns:
            if column in data_frame.columns:
                data_frame[column] = self.__normalize_numeric_series(data_frame[column])

        return data_frame

    def transform_percentage_columns(self, data_frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Transforms percentage columns in the DataFrame to a standard float format."""

        for column in columns:
            if column in data_frame.columns:
                data_frame[column] = self.__normalize_percentage_series(data_frame[column])

        return data_frame

    def transform_date_columns(self, data_frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Transforms date columns in the DataFrame to a standard datetime format."""

        for column in columns:
            if column in data_frame.columns:
                data_frame[column] = pd.to_datetime(data_frame[column], format='%m/%Y', errors='coerce')

        return data_frame

    def transform_categorical_columns(self, data_frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Transforms categorical columns in the DataFrame to a category dtype."""

        for column in columns:
            if column in data_frame.columns:
                data_frame[column] = data_frame[column].astype('category')

        return data_frame

    def transform_text_columns(self, data_frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Transforms text columns in the DataFrame to a string dtype."""

        for column in columns:
            if column in data_frame.columns:
                data_frame[column] = data_frame[column].astype('string').str.strip()

        return data_frame
