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
import pandas as pd

from bacen_ifdata.data_transformer.interfaces.prudential_conglomerates import PrudentialConglomeratesInterface
from bacen_ifdata.data_transformer.parser.bank_consolidation import BankConsolidationTypeParser
from bacen_ifdata.data_transformer.parser.consolidation import ConsolidationTypeParser
from bacen_ifdata.data_transformer.parser.control import ControlTypeParser
from bacen_ifdata.data_transformer.parser.database import DataBaseParser
from bacen_ifdata.data_transformer.parser.financial_institution import FinancialInstitutionParser
from bacen_ifdata.data_transformer.parser.prudential_summary import PrudentialSummaryInformationParser
from bacen_ifdata.data_transformer.parser.segment import SegmentClassificationParser

from bacen_ifdata.data_transformer.schemas.columns_names.prudential_summary import PRUDENTIAL_SUMMARY_SCHEMA


# pylint: disable=missing-class-docstring, missing-function-docstring
class PrudentialConglomeratesTransformer(PrudentialConglomeratesInterface):
    """Converts raw input data into well-organized, structured information
    tailored for prudential conglomerates.
    """

    def __init__(self):
        self.bank_consolidation_type_parser = BankConsolidationTypeParser()
        self.consolidation_type_parser = ConsolidationTypeParser()
        self.control_type_parser = ControlTypeParser()
        self.database_parser = DataBaseParser()
        self.financial_institution_parser = FinancialInstitutionParser()
        self.prudential_summary_information_parser = PrudentialSummaryInformationParser()
        self.segment_classification_parser = SegmentClassificationParser()

    def __normalize_and_parse_numeric_series(self, series: pd.Series) -> pd.Series:
        """Cleans and converts a pandas Series to a numeric type, handling errors gracefully."""

        # Remove non-numeric characters and convert to float.
        if pd.api.types.is_string_dtype(series):
            series = series.str.replace('.', '', regex=False).str.replace(',', '.', regex=False)

        return pd.to_numeric(series, errors='coerce')

    def __apply_business_rules(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Applies specific business rules to the DataFrame."""

        # Capitalizes the city name
        if 'cidade' in data_frame.columns:
            data_frame['cidade'] = data_frame['cidade'].str.title()

        # Fills null values in the segment column
        if 'segmento' in data_frame.columns:
            data_frame['segmento'] = data_frame['segmento'].fillna('Não informado')

        return data_frame

    def __transform_numeric_columns(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Transforms numeric columns in the DataFrame to a standard numeric format."""

        for col in PRUDENTIAL_SUMMARY_SCHEMA.numeric_columns:
            if col in data_frame.columns:
                data_frame[col] = self.__normalize_and_parse_numeric_series(data_frame[col])

        return data_frame

    def __transform_date_columns(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Transforms date columns in the DataFrame to a standard datetime format."""

        for col in PRUDENTIAL_SUMMARY_SCHEMA.date_columns:
            if col in data_frame.columns:
                data_frame[col] = pd.to_datetime(data_frame[col], format='%Y-%m', errors='coerce')

        return data_frame

    def __transform_categorical_columns(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Transforms categorical columns in the DataFrame to a category dtype."""

        for col in PRUDENTIAL_SUMMARY_SCHEMA.categorical_columns:
            if col in data_frame.columns:
                data_frame[col] = data_frame[col].astype('category')

        return data_frame

    def __transform_text_columns(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Transforms text columns in the DataFrame to a string dtype."""

        for col in PRUDENTIAL_SUMMARY_SCHEMA.text_columns:
            if col in data_frame.columns:
                data_frame[col] = data_frame[col].astype('string').str.strip()

        return data_frame

    def transform(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Transforms the input DataFrame into a structured format for prudential conglomerates."""

        # Create a backup copy of the original DataFrame.
        backup_data_frame = data_frame.copy()

        # Transforms numeric columns in the DataFrame to a standard numeric format.
        data_frame = self.__transform_numeric_columns(data_frame)
        # Transforms date columns in the DataFrame to a standard datetime format.
        data_frame = self.__transform_date_columns(data_frame)
        # Transforms categorical columns in the DataFrame to a category dtype.
        data_frame = self.__transform_categorical_columns(data_frame)
        # Transforms text columns in the DataFrame to a string dtype.
        data_frame = self.__transform_text_columns(data_frame)

        # Applies specific business rules to the DataFrame.
        data_frame = self.__apply_business_rules(data_frame)

        return data_frame
