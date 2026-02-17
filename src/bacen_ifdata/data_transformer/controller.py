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

from enum import StrEnum
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from bacen_ifdata.data_transformer.schemas.interfaces import SchemaProtocol
from bacen_ifdata.data_transformer.transformers.base import BaseTransformer
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.utilities.csv_loader import load_csv_data
from bacen_ifdata.utilities.geographic_regions import STATE_TO_REGION as REGION
from bacen_ifdata.utilities.string_utils import slugify


class TransformationType(StrEnum):
    """Supported data transformation types."""

    NUMERIC = 'numeric'
    PERCENTAGE = 'percentage'
    DATE = 'date'
    CATEGORICAL = 'categorical'
    TEXT = 'text'


# Type alias for transformer factory function.
TransformerFactory = Callable[[Institutions], BaseTransformer]


# pylint: disable=too-few-public-methods, missing-function-docstring
class TransformerController:
    """Controller for transforming data from reports.

    This class is responsible for controlling the transformation of data from reports.
    """

    def __init__(self, transformer_factory: TransformerFactory) -> None:
        """Initializes a new instance of the TransformerController class.

        Args:
            transformer_factory (TransformerFactory): A factory function that returns
                the appropriate transformer for a given institution type.
        """

        # Initializing the transformer factory.
        self.transformer_factory = transformer_factory
        # Cache for transformer instances.
        self._transformer_cache: dict[Institutions, BaseTransformer] = {}

    def _get_transformer(self, institution: Institutions) -> BaseTransformer:
        """Gets or creates a transformer for the given institution.

        Args:
            institution (Institutions): The institution type.

        Returns:
            BaseTransformer: The transformer instance.
        """

        if institution not in self._transformer_cache:
            self._transformer_cache[institution] = self.transformer_factory(institution)

        return self._transformer_cache[institution]

    def _build_transformation_map(
        self, transformer: BaseTransformer
    ) -> dict[TransformationType, Callable[[pd.DataFrame, list[str]], pd.DataFrame]]:
        """Builds the transformation map for a given transformer.

        Args:
            transformer (BaseTransformer): The transformer to build the map for.

        Returns:
            dict: Mapping of transformation types to their corresponding methods.
        """

        return {
            TransformationType.NUMERIC: transformer.transform_numeric_columns,
            TransformationType.PERCENTAGE: transformer.transform_percentage_columns,
            TransformationType.DATE: transformer.transform_date_columns,
            TransformationType.CATEGORICAL: transformer.transform_categorical_columns,
            TransformationType.TEXT: transformer.transform_text_columns,
        }

    def _load_data(self, file_path: Path, options: dict[str, Any]) -> pd.DataFrame:
        """Loads the data for transformation.

        This method is responsible for loading the data that will be transformed.

        Args:
            file_path (Path): The path to the CSV file to be loaded.
            options (dict[str, Any]): The options to be used for loading the CSV file.
        """

        return load_csv_data(file_path.as_posix(), options)

    def _create_region_column(self, data: pd.DataFrame) -> pd.DataFrame:
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

    def _build_column_rename_map(self, data: pd.DataFrame, schema: SchemaProtocol) -> dict[str, str]:
        """Builds a mapping from CSV header column names to schema column names.

        Uses Name-Based Mapping (Slugification) to find the correct column.
        This provides robustness against column shifts (e.g. historical data
        having extra columns).

        For schemas with explicit csv_header metadata (used for hierarchical/grouped
        CSV headers), the csv_header value is slugified and used as the lookup key.

        Algorithm:
        1. Slugify all CSV column names to create a lookup map.
        2. Iterate through Schema fields.
        3. If schema field has a csv_header, slugify it and match against CSV slugs.
        4. Otherwise, match Schema field name against the Slugified CSV names.
        5. If found, map "Original CSV Name" -> "Schema Field Name".

        Args:
            data (pd.DataFrame): The loaded DataFrame (with original CSV header).
            schema (SchemaProtocol): The schema definition.

        Returns:
            dict[str, str]: Mapping of CSV column names to schema column names.
        """

        schema_names = schema.input_column_names
        csv_columns = list(data.columns)

        # Create a lookup map: {slugified_col_name: original_col_name}.
        # We use a dictionary to map the normalized name back to the original CSV header.
        csv_slug_map = {slugify(column): column for column in csv_columns}

        rename_map: dict[str, str] = {}

        for schema_field in schema_names:
            # Check if schema defines an explicit CSV header for this field
            csv_header = schema.get_raw_csv_header(schema_field) if hasattr(schema, 'get_raw_csv_header') else None
            lookup_key = slugify(csv_header) if csv_header else schema_field

            # Look up the schema field in the CSV slug map.
            if lookup_key in csv_slug_map:
                original_csv_col = csv_slug_map[lookup_key]

                # Only map if the names are different (Pandas rename optimization).
                if original_csv_col != schema_field:
                    rename_map[original_csv_col] = schema_field
            else:
                # Handle Special Case: 'data' -> 'data_base'
                if schema_field == 'data_base' and 'data' in csv_slug_map:
                    original_csv_col = csv_slug_map['data']
                    rename_map[original_csv_col] = 'data_base'
                    continue

                # Standardize 'instituicao'
                if schema_field == 'instituicao' and 'instituicao_financeira' in csv_slug_map:
                    original_csv_col = csv_slug_map['instituicao_financeira']
                    rename_map[original_csv_col] = 'instituicao'
                    continue

        return rename_map

    def transform(self, file_path: Path, schema: SchemaProtocol, institution: Institutions) -> pd.DataFrame:
        """Transforms data from reports.

        This method is responsible for transforming the data from reports.

        Args:
            file_path (Path): The path to the CSV file to be transformed.
            schema (SchemaProtocol): The schema for the reported.
            institution (Institutions): The institution type.

        Returns:
            pd.DataFrame: The transformed DataFrame.
        """

        # Get the appropriate transformer for this institution.
        transformer = self._get_transformer(institution)

        # Build the transformation map for this transformer.
        transformation_map = self._build_transformation_map(transformer)

        # Configurations for correctly loading the data from CSV file.
        # Processed CSVs now include the normalized header as the first line.
        options = {'sep': ';', 'header': 0, 'dtype': str}

        # Load the data.
        data = self._load_data(file_path, options)

        # Rename CSV header columns to match schema names (positional mapping).
        # Extra columns in the CSV (not covered by the schema) are dropped.
        rename_map = self._build_column_rename_map(data, schema)
        if rename_map:
            data = data.rename(columns=rename_map)

        # Keep only columns defined in the schema (drop extras),
        # ensuring we have the correct columns for transformation.
        schema_columns = [column for column in schema.input_column_names if column in data.columns]
        data = data[schema_columns]

        # Apply business rules, if any.
        data = transformer.apply_business_rules(data)

        # Group dataframe columns by type, consulting the schema.
        columns_by_type: dict[TransformationType, list[str]] = {}
        for column_name in data.columns:
            column_type = schema.get_type(column_name)

            # Map column types to their corresponding transformation functions.
            if column_type:
                columns_by_type.setdefault(column_type, []).append(column_name)

        # Iterate over the grouped column types and apply the correct transformation.
        for column_type, columns in columns_by_type.items():
            transform_function = transformation_map.get(column_type)

            # Call the transformation function, passing the relevant columns
            if transform_function:
                data = transform_function(data, columns)

        # Create the region column based on the state column and insert it after the "uf" column.
        if 'cidade' in data.columns:
            data = self._create_region_column(data)

        return data
