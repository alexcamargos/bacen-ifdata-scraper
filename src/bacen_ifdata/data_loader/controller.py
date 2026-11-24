"""Controller for loading data from reports into the database."""

from datetime import date
from enum import StrEnum
from pathlib import Path

import duckdb as db
from loguru import logger

from bacen_ifdata.data_loader.storage import DatabaseService
from bacen_ifdata.data_transformer.schemas.base_schema import BaseSchema
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


# pylint: disable=too-few-public-methods
class LoaderController:
    """Controller for loading data from reports.

    This class is responsible for controlling the loading of data from reports
    into the database.
    """

    def __init__(self, database_service: DatabaseService | None = None) -> None:
        """Initializes a new instance of the LoaderController class.

        Args:
            database_service (DatabaseService, optional): The database service instance.
                                                          Defaults to a new instance.
        """

        self._database_service = database_service or DatabaseService()

    def load_report(
        self,
        institution: Institutions,
        report: StrEnum,
        input_data: Path,
        schema: BaseSchema,
        *,
        period: date | None = None,
    ) -> None:
        """Load data from the source CSV file into the database.

        Args:
            institution (Institutions): The institution of the report.
            report (StrEnum): The report type.
            input_data (Path): The path to the CSV file to be loaded.
            schema (BaseSchema): The schema to be used for the table.
            period: Reference month to validate and replace inside the
                supplied database service's transaction, when given.

        Returns:
            None.

        Raises:
            ValueError: The input violates the report schema or period.
            OSError: The input cannot be read.
            db.Error: DuckDB cannot create or load the table.
        """

        # Determine table name
        # Format: institution_report (e.g., financial_conglomerates_summary)
        table_name = f'{institution.name.lower()}_{report.name.lower()}'

        logger.info(f'Preparing to load {input_data.name} into table {table_name}...')

        try:
            # Ensure the table exists and has the correct schema/comments
            self._database_service.create_table(table_name, schema)

            # Insert the data
            if period is None:
                self._database_service.insert_data(
                    table_name, input_data, schema
                )
            else:
                self._database_service.replace_period(
                    table_name, input_data, schema, period, source=input_data,
                )

            logger.info(f'Successfully loaded {institution.name} - {report.name}.')

        except db.Error as error:
            logger.error(f'Failed to load {institution.name} - {report.name}: {error}')
            raise
