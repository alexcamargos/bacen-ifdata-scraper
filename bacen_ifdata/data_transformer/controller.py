#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: controller.py
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

from pathlib import Path
from typing import Callable, Dict, List

import pandas as pd

from bacen_ifdata.data_transformer.transformers.interfaces.dataframe_transformer import DataFrameTransformerProtocol
from bacen_ifdata.utilities.csv_loader import load_csv_data
from bacen_ifdata.utilities.geographic_regions import STATE_TO_REGION as REGION


# pylint: disable=too-few-public-methods, missing-function-docstring
class TransformerController:
    """Controller for transforming data from reports.

    This class is responsible for controlling the transformation of data from reports.
    """

    def __init__(self, data_frame_transformer: DataFrameTransformerProtocol):
        # Initializing the transformer interface.
        self.data_frame_transformer = data_frame_transformer

        # Mapping of transformation types to their corresponding methods.
        self.transformation_map: Dict[str, Callable[[pd.DataFrame, List[str]], pd.DataFrame]] = {
            'numeric': self.data_frame_transformer.transform_numeric_columns,
            'percentage': self.data_frame_transformer.transform_percentage_columns,
            'date': self.data_frame_transformer.transform_date_columns,
            'categorical': self.data_frame_transformer.transform_categorical_columns,
            'text': self.data_frame_transformer.transform_text_columns,
        }

    def __load_data(self, file_path: Path, options: dict) -> pd.DataFrame:
        """Loads the data for transformation.

        This method is responsible for loading the data that will be transformed.

        Args:
            file_path (Path): The path to the CSV file to be loaded.
            options (dict): The options to be used for loading the CSV file.
        """

        return load_csv_data(file_path.as_posix(), options)

    def __create_region_column(self, data: pd.DataFrame) -> pd.DataFrame:
        """Creates the region column based on the state column.

        This method is responsible for creating the region column in the DataFrame.

        Args:
            data (pd.DataFrame): The DataFrame to be modified.

        Returns:
            pd.DataFrame: The modified DataFrame with the region column.
        """

        # Create the region column based on the state column.
        uf_column_index = data.columns.get_loc('uf') + 1
        data.insert(uf_column_index, 'regiao', data['uf'].map(REGION))

        return data

    def transform(self, file_path: Path, schema) -> pd.DataFrame:
        """Transforms data from prudential conglomerates reports.

        This method is responsible for transforming the data from prudential conglomerates reports.

        Args:
            file_path (Path): The path to the CSV file to be transformed.
        """

        # Configurations for correctly loading the data from prudential conglomerates CSV file.
        options = {
            'sep': ';',
            'names': schema.column_names,
            'dtype': str
        }

        # Load the data.
        data = self.__load_data(file_path, options)

        # Apply business rules, if any.
        data = self.data_frame_transformer.apply_business_rules(data)

        # Group dataframe columns by type, consulting the schema.
        columns_by_type: Dict[str, List[str]] = {}
        for column_name in data.columns:
            column_type = schema.get_type(column_name)

            # Map column types to their corresponding transformation functions.
            if column_type:
                columns_by_type.setdefault(column_type, []).append(column_name)

        # Iterate over the grouped column types and apply the correct transformation.
        for column_type, columns in columns_by_type.items():
            transform_function = self.transformation_map.get(column_type)

            # Call the transformation function, passing the relevant columns
            if transform_function:
                data = transform_function(data, columns)

        # Create the region column based on the state column and insert it after the "uf" column.
        if 'cidade' in data.columns:
            data = self.__create_region_column(data)

        return data
