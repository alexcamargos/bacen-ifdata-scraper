"""Interfaces for Data Transformer Schemas

This module defines the protocols and interfaces for schema classes used in the
data transformation process.
"""

from typing import Protocol


# pylint: disable=too-few-public-methods
class SchemaProtocol(Protocol):
    """Protocol for schema classes.

    Defines the interface that all schema classes must implement to be compatible
    with the TransformerController.
    """

    @property
    def column_names(self) -> list[str]:
        """Return the list of column names defined in the schema.

        Returns:
            list[str]: A list of column names.
        """

    def get_type(self, column_name: str) -> str | None:
        """Return the type of a specific column from the schema definition.

        Args:
            column_name (str): The name of the column.

        Returns:
            str | None: The type of the column if it exists, otherwise None.
        """
