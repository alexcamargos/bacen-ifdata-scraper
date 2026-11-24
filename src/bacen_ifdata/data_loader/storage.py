"""Database Service module for handling DuckDB operations.

This module provides the DatabaseService class, which is responsible for
managing connections to the DuckDB database, creating tables based on schemas,
and loading data from CSV files.
"""

import csv
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import date
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

        Raises:
            OSError: The CSV cannot be opened.
            csv.Error: The header cannot be parsed.
        """

        with csv_path.open(encoding='utf-8-sig', newline='') as file:
            return next(csv.reader(file), [])

    def _build_insert_query(
        self, table_name: str, csv_path: Path, columns: list[str],
        schema: BaseSchema,
    ) -> str:
        """Builds the DuckDB INSERT query with explicit column types.

        Args:
            table_name (str): The name of the target table.
            csv_path (Path): The path to the CSV file.
            columns (list[str]): The list of columns to import.
            schema (BaseSchema): The schema defining column types.

        Returns:
            str: The SQL query string.

        Raises:
            None.
        """

        columns_struct = []
        projections = []
        for column_name in columns:
            column_type = schema.get_type(column_name)
            duckdb_type = self._map_type_to_duckdb(column_type)
            identifier = f'"{column_name}"'
            if column_type == 'integer':
                # DuckDB can round fractional CSV values when reading BIGINT.
                columns_struct.append(f"'{column_name}': 'VARCHAR'")
                value = f'trim({identifier})'
                projections.append(
                    f"CASE WHEN NOT regexp_full_match({value}, "
                    f"'[+-]?[0-9]+([.]0+)?') "
                    f"THEN error('Expected an integer in {column_name}') "
                    f"ELSE CAST(split_part({value}, '.', 1) AS BIGINT) END"
                )
            else:
                columns_struct.append(f"'{column_name}': '{duckdb_type}'")
                projections.append(identifier)

        columns_str = ", ".join(columns_struct)
        column_names_str = ", ".join([f'"{col}"' for col in columns])
        projection = ', '.join(projections)
        csv_literal = csv_path.as_posix().replace("'", "''")

        return (
            f"INSERT INTO {table_name} ({column_names_str}) "
            f"SELECT {projection} FROM read_csv("
            f"'{csv_literal}', "
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

    @contextmanager
    def transaction(self) -> Iterator[db.DuckDBPyConnection]:
        """Commit the enclosed mutations together or roll them back.

        Args:
            None.

        Yields:
            The connection participating in the transaction.

        Returns:
            None.

        Raises:
            db.Error: DuckDB cannot execute a transaction operation.
        """
        connection = self.connection
        connection.begin()
        committed = False
        try:
            yield connection
            connection.commit()
            committed = True
        finally:
            if not committed:
                connection.rollback()

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

    def drop_table(self, table_name: str) -> None:
        """Drop a specific table if it exists.

        Args:
            table_name (str): The name of the table to drop.
        """

        try:
            self.connection.execute(f'DROP TABLE IF EXISTS "{table_name}";')
            logger.info(f"Table '{table_name}' dropped specifically.")
        except db.Error as error:
            logger.error(f"Error dropping table '{table_name}': {error}")
            raise

    def create_table(self, table_name: str, schema: BaseSchema) -> None:
        """Create a table in the database if it does not exist.

        Args:
            table_name (str): The name of the table to create.
            schema (BaseSchema): The schema definition for the table.

        Returns:
            None.

        Raises:
            db.Error: DuckDB cannot create or annotate the table.
        """

        columns_definitions = []
        comments = []

        for column_name in schema.column_names:
            column_type = schema.get_type(column_name)
            duckdb_type = self._map_type_to_duckdb(column_type)

            # Sanitize column name to avoid SQL injection or syntax errors
            # Assuming column names are already relatively safe, but quoting is good practice.
            safe_column_name = f'"{column_name}"'
            constraint = (
                ' NOT NULL' if column_name in schema.required_input_columns
                else ''
            )
            columns_definitions.append(
                f'{safe_column_name} {duckdb_type}{constraint}'
            )

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

        Returns:
            None.

        Raises:
            ValueError: A required CSV column is missing or repeated.
            OSError: The CSV cannot be read.
            csv.Error: The header cannot be parsed.
            db.Error: DuckDB cannot parse or insert the rows.
        """

        try:
            # Read CSV header to identify present columns
            raw_columns = self._get_raw_csv_header(csv_path)
            schema.validate_required_columns(raw_columns, csv_path)

            # DuckDB binds explicit CSV types by position.
            common_columns = [
                column for column in raw_columns
                if column in schema.column_names
            ]

            if not common_columns:
                logger.warning(f"No matching columns found between schema and '{csv_path.name}'. Skipping.")
                return

            # Build and execute the query
            query = self._build_insert_query(table_name, csv_path, common_columns, schema)
            self.connection.execute(query)
            logger.info(f"Data from '{csv_path.name}' loaded into '{table_name}' ({len(common_columns)} columns).")

        except (OSError, csv.Error, db.Error) as error:
            logger.error(f"Error loading data from '{csv_path}' into '{table_name}': {error}")
            raise

    def replace_period(
        self,
        table: str,
        csv_path: Path,
        schema: BaseSchema,
        period: date,
        *,
        source: Path,
    ) -> int:
        """Replace a complete report month inside the caller's transaction.

        Args:
            table: Canonical Silver report table.
            csv_path: Transformed CSV to read.
            schema: Report schema used to parse the CSV.
            period: First day of the reference month.
            source: Original path to include in validation errors.

        Returns:
            Number of rows inserted for the period.

        Raises:
            ValueError: Required columns or the period's keys are invalid.
            OSError: The transformed CSV cannot be read.
            csv.Error: The header cannot be parsed.
            db.Error: DuckDB cannot stage or replace the data.
        """
        connection = self.connection
        connection.execute(
            f'CREATE TEMP TABLE ifdata_input AS SELECT * FROM {table} LIMIT 0'
        )
        self.insert_data('ifdata_input', csv_path, schema)
        rows, codes, dated = connection.execute(
            'SELECT count(*), count(DISTINCT codigo), '
            'count(*) FILTER (WHERE data_base = ?) FROM ifdata_input',
            [period],
        ).fetchone()
        if not rows or rows != codes or rows != dated:
            raise ValueError(
                f'{source}: expected unique institution codes and data-base '
                f'{period:%Y-%m}. Found {rows} rows, {codes} distinct codes '
                f'and {dated} rows for the expected month.'
            )
        connection.execute(
            f'DELETE FROM {table} WHERE data_base = ?', [period]
        )
        connection.execute(f'INSERT INTO {table} SELECT * FROM ifdata_input')
        connection.execute('DROP TABLE ifdata_input')
        return rows
