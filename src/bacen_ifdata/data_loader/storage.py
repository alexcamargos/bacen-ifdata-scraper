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
        self, database_path: Path = Config.SILVER_DATABASE_FILE, connection: db.DuckDBPyConnection | None = None
    ) -> None:
        """Initialize the DatabaseService.

        Args:
            database_path (Path): Path to the DuckDB database file. Defaults to Config.SILVER_DATABASE_FILE.
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

    def _get_raw_csv_header(self, csv_path: Path) -> list[str]:
        """Reads the CSV header to identify present columns.

        Args:
            csv_path (Path): The path to the CSV file.

        Returns:
            list[str]: A list of column names found in the CSV header.
        """

        with open(csv_path, 'r', encoding='utf-8') as file:
            header_line = file.readline().strip()
            # Handle potential BOM
            if header_line.startswith('\ufeff'):
                header_line = header_line[1:]

            # Simple CSV split assuming standard comma delimiter and quotes
            return [column.strip().strip('"') for column in header_line.split(',')]

    def _build_insert_query(self, table_name: str, csv_path: Path, columns: list[str], schema: BaseSchema) -> str:
        """Builds the DuckDB INSERT query with explicit column types.

        Args:
            table_name (str): The name of the target table.
            csv_path (Path): The path to the CSV file.
            columns (list[str]): The list of columns to import.
            schema (BaseSchema): The schema defining column types.

        Returns:
            str: The SQL query string.
        """

        columns_struct = []
        for column_name in columns:
            column_type = schema.get_type(column_name)
            duckdb_type = self._map_type_to_duckdb(column_type)
            columns_struct.append(f"'{column_name}': '{duckdb_type}'")

        columns_str = ", ".join(columns_struct)
        column_names_str = ", ".join([f'"{col}"' for col in columns])

        return (
            f"INSERT INTO {table_name} ({column_names_str}) SELECT * FROM read_csv("
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

    def reset_database(self) -> None:
        """Drop all existing tables to prepare for a full data reload.

        This must be called once before the loading loop begins, since the
        pipeline performs a full reload on each execution. Individual
        ``create_table`` calls must NOT drop tables because each report
        type appends multiple CSV files to the same table.
        """

        try:
            tables = self.connection.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
            ).fetchall()

            for (table_name,) in tables:
                self.connection.execute(f'DROP TABLE IF EXISTS "{table_name}";')

            logger.info(f"Database reset: {len(tables)} table(s) dropped.")

        except db.Error as error:
            logger.error(f"Error resetting database: {error}")
            raise

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
            # Read CSV header to identify present columns
            raw_columns = self._get_raw_csv_header(csv_path)

            # Intersect schema columns with CSV columns to maintain order and validity
            common_columns = [column for column in schema.column_names if column in raw_columns]

            if not common_columns:
                logger.warning(f"No matching columns found between schema and '{csv_path.name}'. Skipping.")
                return

            # Build and execute the query
            query = self._build_insert_query(table_name, csv_path, common_columns, schema)
            self.connection.execute(query)
            logger.info(f"Data from '{csv_path.name}' loaded into '{table_name}' ({len(common_columns)} columns).")

        except (OSError, db.Error) as error:
            logger.error(f"Error loading data from '{csv_path}' into '{table_name}': {error}")
            raise
