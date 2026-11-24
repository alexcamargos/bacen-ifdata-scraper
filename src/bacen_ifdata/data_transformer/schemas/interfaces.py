"""Interfaces for Data Transformer Schemas

This module defines the protocols and interfaces for schema classes used in the
data transformation process.
"""

from collections.abc import Iterable
from pathlib import Path
from typing import Protocol


# pylint: disable=too-few-public-methods
class SchemaProtocol(Protocol):
    """Protocol for schema classes.

    Defines the interface that all schema classes must implement to be compatible
    with the TransformerController.
    """

    input_column_names: list[str]

    @property
    def column_names(self) -> list[str]:
        """Return the list of column names defined in the schema.

        Returns:
            list[str]: A list of column names.
        """

    @property
    def required_input_columns(self) -> tuple[str, ...]:
        """Return the required source columns for a report.

        Args:
            None.

        Returns:
            Canonical names of the required input columns.

        Raises:
            None.
        """

    def validate_required_columns(
        self, columns: Iterable[str], source: Path
    ) -> None:
        """Check the required columns in a canonical CSV header.

        Args:
            columns: Canonical column names in the input.
            source: Path of the input file.

        Returns:
            None.

        Raises:
            ValueError: A required column is missing or repeated.
        """

    def get_type(self, column_name: str) -> str | None:
        """Return the type of a specific column from the schema definition.

        Args:
            column_name (str): The name of the column.

        Returns:
            str | None: The type of the column if it exists, otherwise None.
        """
