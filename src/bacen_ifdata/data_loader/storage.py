"""Database Service module for handling DuckDB operations.

This module provides the DatabaseService class, which is responsible for
managing connections to the DuckDB database, creating tables based on schemas,
and loading data from CSV files.
"""

from pathlib import Path

import duckdb as db
from loguru import logger

from bacen_ifdata.data_transformer.schemas.base_schema import BaseSchema
from bacen_ifdata.utilities.configurations import Config


class DatabaseService:
    """Manages DuckDB database operations."""

    def __init__(
        self, database_path: Path = Config.DATABASE_FILE, connection: db.DuckDBPyConnection | None = None
    ) -> None:
        """Initialize the DatabaseService.

        Args:
            database_path (Path): Path to the DuckDB database file. Defaults to Config.DATABASE_FILE.
            connection (duckdb.DuckDBPyConnection | None): An existing database connection.
                                                           Defaults to None, in which case a new connection will
                                                           be established when needed.
        """

        self._database_path = database_path
        self._connection = connection

    def _map_type_to_duckdb(self, schema_type: str | None) -> str:
        """Map internal schema types to DuckDB types.

        Args:
            schema_type (str | None): The schema type to map.

        Returns:
            str: The corresponding DuckDB type.
        """

        if schema_type in ('numeric', 'percentage', 'currency'):
            return 'DOUBLE'

        if schema_type == 'integer':
            return 'BIGINT'  # Use BIGINT to be safe with large numbers

        if schema_type == 'date':
            return 'DATE'

        if schema_type == 'boolean':
            return 'BOOLEAN'

        # Default to VARCHAR for text, categorical, and unknown types
        return 'VARCHAR'

    @property
    def connection(self) -> db.DuckDBPyConnection:
        """Get the active database connection.

        Returns:
            duckdb.DuckDBPyConnection: The active database connection.
        """

        if self._connection is None:
            self._connection = db.connect(str(self._database_path))

        return self._connection

    def close(self) -> None:
        """Close the database connection."""

        if self._connection:
            self._connection.close()
            self._connection = None

    def create_table(self, table_name: str, schema: BaseSchema) -> None:
        """Create a table in the database if it does not exist.

        Args:
            table_name (str): The name of the table to create.
            schema (BaseSchema): The schema definition for the table.
        """

        columns_definitions = []
        comments = []

        for column_name in schema.column_names:
            column_type = schema.get_type(column_name)
            duckdb_type = self._map_type_to_duckdb(column_type)

            # Sanitize column name to avoid SQL injection or syntax errors
            # Assuming column names are already relatively safe, but quoting is good practice.
            safe_column_name = f'"{column_name}"'
            columns_definitions.append(f'{safe_column_name} {duckdb_type}')

            description = schema.get_description(column_name)
            if description:
                # Escape single quotes in description
                safe_description = description.replace("'", "''")
                comments.append(f"COMMENT ON COLUMN {table_name}.{safe_column_name} IS '{safe_description}';")

        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_definitions)});"

        try:
            self.connection.execute(create_query)
            logger.info(f"Table '{table_name}' checked/created successfully.")

            # Apply comments
            for comment in comments:
                self.connection.execute(comment)

        except db.Error as error:
            logger.error(f"Error creating table '{table_name}': {error}")
            raise

    def insert_data(self, table_name: str, csv_path: Path, schema: BaseSchema) -> None:
        """Insert data from a CSV file into the specified table.

        Uses DuckDB's read_csv with explicit column types to avoid sniffing errors.

        Args:
            table_name (str): The name of the target table.
            csv_path (Path): The path to the CSV file.
            schema (BaseSchema): The schema defining column types.
        """

        try:
            # Build the columns dictionary string for read_csv
            # Format: {'col1': 'TYPE', 'col2': 'TYPE', ...}
            columns_struct = []
            for column_name in schema.column_names:
                column_type = schema.get_type(column_name)
                duckdb_type = self._map_type_to_duckdb(column_type)
                columns_struct.append(f"'{column_name}': '{duckdb_type}'")

            columns_str = ", ".join(columns_struct)

            # Use INSERT INTO ... SELECT ... FROM read_csv(...)
            # valid_types='ALL' might be needed if date parsing is strict, but let's try standard first.
            # dateformat='%Y-%m-%d' matches standard ISO.
            query = (
                f"INSERT INTO {table_name} SELECT * FROM read_csv("
                f"'{csv_path.as_posix()}', "
                f"header=True, "
                f"delim=',', "
                f"quote='\"', "
                f"escape='\"', "
                f"columns={{{columns_str}}}, "
                f"dateformat='%Y-%m-%d', "
                f"null_padding=True, "
                f"nullstr=['', 'NULL', 'NA', 'N/A', '-'], "
                f"ignore_errors=False, "
                f"auto_detect=False"
                f");"
            )

            self.connection.execute(query)
            logger.info(f"Data from '{csv_path.name}' loaded into '{table_name}'.")

        except db.Error as error:
            logger.error(f"Error loading data from '{csv_path}' into '{table_name}': {error}")
            raise
