#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: base_schema.py
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

Base schema for data transformation with column metadata and categorization.

Author: Alexsander Lopes Camargos
License: MIT
"""

from functools import cached_property
from typing import Any


class BaseSchema:
    """Base schema class for data transformation.

    This class provides a structure for defining and categorizing column names
    for financial reports, enriched with metadata from the data dictionary.

    Attributes:
        SCHEMA_DEFINITION (dict): A dictionary defining the schema, to be overridden by subclasses.
    """

    # Schema definition dictionary to be overridden by subclasses.
    SCHEMA_DEFINITION: dict[str, dict[str, Any]] = {}

    def _get_columns_by_type(self, column_type: str) -> list[str]:
        """Helper method to get columns by their type.

        Args:
            column_type (str): The type of columns to retrieve.

        Returns:
            list[str]: A list of column names matching the specified type.
        """

        return [
            column_name
            for column_name, attributes in self.SCHEMA_DEFINITION.items()
            if attributes.get('type') == column_type
        ]

    @cached_property
    def column_names(self) -> list[str]:
        """Return all column names defined in the schema."""

        return list(self.SCHEMA_DEFINITION.keys())

    @cached_property
    def numeric_columns(self) -> list[str]:
        """Return dynamically the numeric columns."""

        return self._get_columns_by_type('numeric')

    @cached_property
    def percentage_columns(self) -> list[str]:
        """Return dynamically the percentage columns."""

        return self._get_columns_by_type('percentage')

    @cached_property
    def date_columns(self) -> list[str]:
        """Return dynamically the date columns."""

        return self._get_columns_by_type('date')

    @cached_property
    def categorical_columns(self) -> list[str]:
        """Return dynamically the categorical columns."""

        return self._get_columns_by_type('categorical')

    @cached_property
    def text_columns(self) -> list[str]:
        """Return dynamically the text columns."""

        return self._get_columns_by_type('text')

    def get_type(self, column_name: str) -> str | None:
        """Return the type of a specific column from the schema definition.

        Args:
            column_name (str): The name of the column to retrieve the type for.

        Returns:
            str | None: The type of the column if it exists, otherwise None.
        """

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('type')

    def get_description(self, column_name: str) -> str | None:
        """Return the description of a specific column.

        Args:
            column_name (str): The name of the column to retrieve the description for.

        Returns:
            str | None: The description of the column if it exists, otherwise None.
        """

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('description')

    def get_mapping(self, column_name: str) -> dict | None:
        """Return the mapping dictionary for a categorical column if it exists.

        Args:
            column_name (str): The name of the column to retrieve the mapping for.

        Returns:
            dict | None: The mapping dictionary if it exists, otherwise None.
        """

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('mapping')
