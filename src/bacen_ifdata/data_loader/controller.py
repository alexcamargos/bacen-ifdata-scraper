#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: loader.py
#  Version: 0.0.1
#
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
# ------------------------------------------------------------------------------

"""Bacen IF.data AutoScraper & Data Manager"""

from pathlib import Path
from typing import Any, Optional

import pandas as pd
from loguru import logger

from bacen_ifdata.data_transformer.schemas.interfaces import SchemaProtocol
from bacen_ifdata.utilities.csv_loader import load_csv_data


# pylint: disable=too-few-public-methods
class LoaderController:
    """Controller for loading data from reports.

    This class is responsible for controlling the loading of data from reports.
    """

    def __init__(self) -> None:
        """Initializes a new instance of the LoaderController class."""

        self._data: Optional[pd.DataFrame] = None

    def _load_data(self, csv_file_path: Path, schema: SchemaProtocol) -> None:
        """Load data from the source CSV file.

        This method is responsible for loading the data from the source CSV file.

        Args:
            csv_file_path (Path): The path to the CSV file to be loaded.
            schema (SchemaProtocol): The schema to be used for loading the data.
        """

        # Map schema types to pandas dtypes.
        dtype_map: dict[str, str] = {}
        parse_dates: list[str] = []

        for column_name, definition in schema.SCHEMA_DEFINITION.items():
            data_type = definition.get('type')
            if data_type in ('numeric', 'percentage'):
                dtype_map[column_name] = 'float64'
            elif data_type == 'categorical':
                dtype_map[column_name] = 'category'
            elif data_type == 'date':
                parse_dates.append(column_name)
            else:
                dtype_map[column_name] = 'object'

        csv_options: dict[str, Any] = {
            'sep': ',',
            'header': 0,
            'dtype': dtype_map,
            'parse_dates': parse_dates,
        }

        # Load the data from the input CSV file.
        self._data = load_csv_data(csv_file_path.as_posix(), csv_options)

    def loader_sample_data(self, input_data: Path, schema: SchemaProtocol, sample_size: int = 5) -> None:
        """Load a sample of the data

        This method loads a sample of the data from the input CSV file and prints it.

        Args:
            input_data (Path): The path to the CSV file to be loaded.
            schema (SchemaProtocol): The schema to be used for loading the data.
            sample_size (int): The number of sample rows to be printed. Default is 5.
        """

        # Load the data from the input CSV file.
        self._load_data(input_data, schema)

        # Check if the data was loaded successfully.
        if self._data is None:
            raise RuntimeError("Data loading failed: self._data is None")

        # Print a sample of the loaded data.
        logger.info(self._data.sample(sample_size))
        logger.info(f'Total rows loaded: {len(self._data)}')
        logger.info(f'Total columns loaded: {len(self._data.columns)}')

