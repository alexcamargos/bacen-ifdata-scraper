#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: base.py
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
Base Transformer for Bacen IF.data

This module defines the BaseTransformer class, which provides common data transformation
methods used across different report types.
"""

import pandas as pd


class BaseTransformer:
    """Base class for data transformers, providing common normalization and transformation methods."""

    def _normalize_percentage_series(self, series: pd.Series) -> pd.Series:
        """Removes the '%' sign from a pandas Series and converts it to float.

        Args:
            series (pd.Series): The pandas Series containing percentage values as strings.

        Returns:
            pd.Series: A pandas Series with float values representing the percentages.
        """

        series_cleaned = series.str.replace('%', '', regex=False).str.replace(',', '.', regex=False)

        return pd.to_numeric(series_cleaned, errors='coerce') / 100

    def _normalize_numeric_series(self, series: pd.Series) -> pd.Series:
        """Cleans and converts a pandas Series to a numeric type, handling errors gracefully.

        Args:
            series (pd.Series): The pandas Series containing numeric values as strings.

        Returns:
            pd.Series: A pandas Series with numeric values.
        """

        # If the series contains decimal values, normalize them.
        series_cleaned = series.str.replace('.', '', regex=False).str.replace(',', '.', regex=False)

        # Convert the cleaned series to numeric, rounding and converting to Int64.
        numeric_series = pd.to_numeric(series_cleaned, errors='coerce')

        return numeric_series.round().astype('Int64')

    def apply_business_rules(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Applies specific business rules to the DataFrame.

        This method is intended to be overridden by subclasses to apply specific logic.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be processed.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """

        return data_frame

    def transform_numeric_columns(self, data_frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Transforms numeric columns in the DataFrame to a standard numeric format.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be processed.
            columns (list[str]): The list of column names to be transformed.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """

        for column in columns:
            if column in data_frame.columns:
                data_frame[column] = self._normalize_numeric_series(data_frame[column])

        return data_frame

    def transform_percentage_columns(self, data_frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Transforms percentage columns in the DataFrame to a standard float format.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be processed.
            columns (list[str]): The list of column names to be transformed.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """

        for column in columns:
            if column in data_frame.columns:
                data_frame[column] = self._normalize_percentage_series(data_frame[column])

        return data_frame

    def transform_date_columns(self, data_frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Transforms date columns in the DataFrame to a standard datetime format.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be processed.
            columns (list[str]): The list of column names to be transformed.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """

        for column in columns:
            if column in data_frame.columns:
                data_frame[column] = pd.to_datetime(data_frame[column], format='%m/%Y', errors='coerce')

        return data_frame

    def transform_categorical_columns(self, data_frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Transforms categorical columns in the DataFrame to a category dtype.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be processed.
            columns (list[str]): The list of column names to be transformed.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """

        for column in columns:
            if column in data_frame.columns:
                data_frame[column] = data_frame[column].astype('category')

        return data_frame

    def transform_text_columns(self, data_frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Transforms text columns in the DataFrame to a string dtype.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be processed.
            columns (list[str]): The list of column names to be transformed.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """

        for column in columns:
            if column in data_frame.columns:
                data_frame[column] = data_frame[column].astype('string').str.strip()

        return data_frame
