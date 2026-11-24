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

        Raises:
            None.
        """

        series_cleaned = series.str.replace('%', '', regex=False)
        has_decimal_comma = series_cleaned.str.contains(',', na=False)
        localized = (
            series_cleaned.str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
        series_cleaned = series_cleaned.mask(has_decimal_comma, localized)

        return pd.to_numeric(series_cleaned, errors='coerce') / 100

    def _normalize_numeric_text(self, series: pd.Series) -> pd.Series:
        """Normalize the decimal and thousands separators of IF.data values.

        Args:
            series: A series containing values in Brazilian notation.

        Returns:
            Numeric strings normalized for parsing, with nulls preserved.

        Raises:
            None.
        """
        return (
            series.astype('string').str.strip()
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )

    def _remove_exact_duplicates(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Removes exact duplicates (character by character replication).

        Args:
            data_frame (pd.DataFrame): The DataFrame to be processed.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """

        return data_frame.drop_duplicates(keep='first').copy()

    def _get_identifier_columns(self, data_frame: pd.DataFrame) -> list[str]:
        """Identifies columns that act as identifiers.

        This method looks for common identifier columns based on the expected schema.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be analyzed.

        Returns:
            list[str]: A list of column names that act as identifiers.
        """

        candidate_identifier_columns = [
            'codigo',
            'instituicao',
            'data_base',
            'tcb',
            'segmento_resolucao',
            'tipo_de_consolidacao',
            'tipo_de_controle',
            'cidade',
            'uf',
            'regiao',
        ]
        return [column for column in candidate_identifier_columns if column in data_frame.columns]

    def _get_financial_columns(self, data_frame: pd.DataFrame, identifier_columns: list[str]) -> list[str]:
        """Identifies columns that contain financial data.

        This method assumes that financial columns are those that are not identified as ID columns.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be analyzed.
            identifier_columns (list[str]): The list of identifier columns.

        Returns:
            list[str]: A list of column names that contain financial data.
        """

        return [column for column in data_frame.columns if column not in identifier_columns]

    def _remove_redundant_empty_rows(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Removes rows where all financial columns are NaN, but ONLY if there is
        another valid row for the same institution on the same date.

        This method identifies rows that are "empty of financial data" (i.e., all financial columns are NaN)
        and checks if there are other rows with the same 'codigo' and 'data_base' that contain financial data.
        If such rows exist, the empty row is considered redundant and is removed.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be processed.
        Returns:
            pd.DataFrame: The processed DataFrame with redundant empty rows removed.
        """

        identifier_columns = self._get_identifier_columns(data_frame)

        # We need at least 'codigo' and 'data_base' to determine redundancy.
        if 'codigo' not in identifier_columns or 'data_base' not in identifier_columns:
            return data_frame

        financial_columns = self._get_financial_columns(data_frame, identifier_columns)

        if not financial_columns:
            return data_frame

        # A row is "empty of financial data" if all financial columns are NA.
        is_financial_empty = data_frame[financial_columns].isna().all(axis=1)

        # If no empty rows, return early.
        if not is_financial_empty.any():
            return data_frame

        # Work on a copy to avoid SettingWithCopy warnings.
        df_processed = data_frame.copy()
        df_processed['__is_financial_empty'] = is_financial_empty

        # Count total rows per institution per date.
        df_processed['__group_count'] = df_processed.groupby(['codigo', 'data_base'])['codigo'].transform('count')

        # Drop rule: If financial data is empty AND group count > 1, drop it.
        rows_to_remove_mask = df_processed['__is_financial_empty'] & (df_processed['__group_count'] > 1)

        return df_processed[~rows_to_remove_mask].drop(columns=['__is_financial_empty', '__group_count'])

    def deduplicate_dataset(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Removes exact duplicates and empty rows that have a populated counterpart.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be deduplicated.

        Returns:
            pd.DataFrame: The deduplicated DataFrame.
        """

        if data_frame.empty:
            return data_frame

        # Remove exact duplicates first to ensure we are working with a clean dataset.
        clean_df = self._remove_exact_duplicates(data_frame)

        # Remove redundant empty rows based on the presence of valid rows for the same institution and date.
        clean_df = self._remove_redundant_empty_rows(clean_df)

        return clean_df

    def transform_numeric_columns(
        self, data_frame: pd.DataFrame, columns: list[str]
    ) -> pd.DataFrame:
        """Parse measures with their original fractional values.

        Args:
            data_frame: The report data.
            columns: Names of the numeric measure columns.

        Returns:
            The report with numeric values and nullable unavailable measures.

        Raises:
            None.
        """

        for column in columns:
            if column in data_frame.columns:
                normalized = self._normalize_numeric_text(data_frame[column])
                data_frame[column] = pd.to_numeric(
                    normalized, errors='coerce'
                )

        return data_frame

    def transform_integer_columns(
        self, data_frame: pd.DataFrame, columns: list[str]
    ) -> pd.DataFrame:
        """Parse nullable whole numbers without a floating-point conversion.

        Args:
            data_frame: The report data.
            columns: Names of integer columns such as identifiers and counts.

        Returns:
            The report with integer values and nullable unavailable values.

        Raises:
            ValueError: A number has a fractional part or exceeds Int64 range.
        """
        for column in columns:
            if column not in data_frame.columns:
                continue
            normalized = self._normalize_numeric_text(data_frame[column])
            whole_numbers = normalized.str.replace(r'\.0+$', '', regex=True)
            if whole_numbers.str.fullmatch(r'[+-]?\d+\.\d+', na=False).any():
                raise ValueError(f'{column!r} must contain whole numbers.')
            valid = whole_numbers.str.fullmatch(r'[+-]?\d+', na=False)
            try:
                data_frame[column] = whole_numbers.where(valid).astype('Int64')
            except (ValueError, OverflowError) as error:
                raise ValueError(f'{column!r} must fit in Int64.') from error

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

    def apply_business_rules(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Applies specific business rules to the DataFrame.

        This method is intended to be overridden by subclasses to apply specific logic.

        Args:
            data_frame (pd.DataFrame): The DataFrame to be processed.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """

        return data_frame
