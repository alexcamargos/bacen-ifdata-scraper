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

import pandas as pd

from bacen_ifdata.data_transformer.schemas import (PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA,
                                                   PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA,
                                                   PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA)
from bacen_ifdata.data_transformer.transformers.prudential_conglomerates import PrudentialConglomeratesTransformer
from bacen_ifdata.utilities.csv_loader import load_csv_data
from bacen_ifdata.utilities.geographic_regions import STATE_TO_REGION as REGION


# pylint: disable=too-few-public-methods, missing-function-docstring
class TransformerController:
    """Controller for transforming data from reports.

    This class is responsible for controlling the transformation of data from reports.
    """

    def __init__(self):
        # Initializing the PrudentialConglomeratesTransformer interface.
        self.prudential_conglomerates_transformer = PrudentialConglomeratesTransformer()

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

    def transform_prudential_conglomerate_summary(self, file_path: Path) -> pd.DataFrame:
        """Transforms data from prudential conglomerates reports.

        This method is responsible for transforming the data from prudential conglomerates reports.

        Args:
            file_path (Path): The path to the CSV file to be transformed.
        """

        # Configurations for correctly loading the data from prudential conglomerates CSV file.
        options = {
            'sep': ';',
            'names': PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA.column_names,
            'dtype': str
        }

        # Load the data.
        data = self.__load_data(file_path, options)

        # Create the region column based on the state column and insert it after the "uf" column.
        data = self.__create_region_column(data)

        return self.prudential_conglomerates_transformer.transform_summary(data)

    def transform_prudential_conglomerate_assets(self, file_path: Path) -> pd.DataFrame:
        """Transforms data from prudential conglomerates reports.

        This method is responsible for transforming the data from prudential conglomerates reports.

        Args:
            file_path (Path): The path to the CSV file to be transformed.
        """

        # Configurations for correctly loading the data from prudential conglomerates CSV file.
        options = {
            'sep': ';',
            'names': PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA.column_names,
            'dtype': str
        }

        # Load the data.
        data = self.__load_data(file_path, options)

        # Create the region column based on the state column and insert it after the "uf" column.
        data = self.__create_region_column(data)

        return self.prudential_conglomerates_transformer.transform_assets(data)

    def transform_prudential_conglomerate_liabilities(self, file_path: Path) -> pd.DataFrame:
        """Transforms data from prudential conglomerates reports.

        This method is responsible for transforming the data from prudential conglomerates reports.

        Args:
            file_path (Path): The path to the CSV file to be transformed.
        """

        # Configurations for correctly loading the data from prudential conglomerates CSV file.
        options = {
            'sep': ';',
            'names': PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA.column_names,
            'dtype': str
        }

        # Load the data.
        data = self.__load_data(file_path, options)

        # Create the region column based on the state column and insert it after the "uf" column.
        data = self.__create_region_column(data)

        return self.prudential_conglomerates_transformer.transform_liabilities(data)
