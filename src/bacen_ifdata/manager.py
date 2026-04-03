#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: manager.py
#  Version: 0.0.1
#
#  Summary: Project Name
#           Quick description of the project.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

import os
import subprocess
from enum import StrEnum
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from bacen_ifdata import Pipeline
from bacen_ifdata.data_loader.storage import DatabaseService
from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.scraper.storage.processing import build_directory_path
from bacen_ifdata.scraper.utils import validate_report_selection
from bacen_ifdata.utilities.clean import clean_download_base_directory, clean_empty_csv_files
from bacen_ifdata.utilities.configurations import Config as Cfg


class PipelineManager:
    """Manages the IF.data pipeline, including scraping, cleaning, transforming, and loading data."""

    def __init__(self, pipeline: Pipeline, database_service: DatabaseService | None = None) -> None:
        """Initializes the PipelineManager with a pipeline instance.

        Args:
            pipeline (Pipeline): An instance of the Pipeline class.
            database_service (DatabaseService | None): An optional instance of DatabaseService for managing database
                                                       connections. If not provided, a new instance will be created
                                                       when needed.
        """

        # The Pipeline class orchestrates the entire data processing workflow,
        # including scraping, cleaning, transforming, and loading data.
        self.pipeline = pipeline
        # The DatabaseService is responsible for managing the connection to the DuckDB database.
        self._database_service = database_service or DatabaseService()

    def _clean_download_directory(self) -> None:
        """Performs comprehensive cleaning operations on the download directory.

        This function orchestrates a two-step cleaning process:
        1. It first removes all empty CSV files from the download directory.
        This step helps in eliminating files that were downloaded but contain
        no data, possibly due to errors in the data scraping process.
        2. Then, it cleans up the download base directory by removing any
        remaining CSV files. This is typically done to prepare for a fresh start,
        ensuring that no outdated or unnecessary files remain that could interfere
        with subsequent scraping sessions.

        The cleaning process targets the directory specified in the configuration's DOWNLOAD_DIRECTORY,
        using paths built from the configuration settings. Messages are printed to the console to
        indicate the progress of cleaning operations.
        """

        # Clean up the empty CSV files in the download directory.
        logger.info('Cleaning up empty CSV files...')
        clean_empty_csv_files(build_directory_path(Cfg.DOWNLOAD_DIRECTORY))

        # Clean up the download base directory.
        logger.info('Cleaning up the download base directory...')
        clean_download_base_directory(build_directory_path(Cfg.DOWNLOAD_DIRECTORY))

    def _reset_database(self) -> None:
        """Resets the database before loading to prevent data duplication.

        The pipeline performs a full reload on each execution.
        """

        self._database_service.reset_database()
        self._database_service.close()

    def _get_execution_targets(
        self, institution_filter: str | None = None, report_filter: str | None = None
    ) -> list[tuple[Institutions, StrEnum]]:
        """Determine which institutions and reports to process based on filters.

        Args:
            institution_filter: Optional name of the institution Enum to filter by.
            report_filter: Optional name of the report Enum to filter by.

        Returns:
            A list of tuples (Institution, Report) to process.
        """

        targets = []

        # Find matching institution enum if filter provided
        target_inst = None
        if institution_filter:
            try:
                # Get the enum member by its name (e.g. 'PRUDENTIAL_CONGLOMERATES')
                target_inst = Institutions[institution_filter.upper()]
            except KeyError:
                logger.warning(f"Institution filter '{institution_filter}' not found. Ignoring filter.")

        for institution in Institutions:
            if target_inst and institution != target_inst:
                continue

            for report in REPORTS[institution]:
                if report_filter and report.name.upper() != report_filter.upper():
                    continue

                targets.append((institution, report))

        return targets

    def run_scraper(self, institution: str | None = None, report: str | None = None) -> None:
        """Main function for executing the scraper."""

        if self.pipeline.session is None:
            raise ValueError('Session is not initialized.')

        try:
            # Get the available data bases.
            data_base: list[str] = self.pipeline.session.get_data_bases()

            # Run the scraper...
            targets = self._get_execution_targets(institution, report)
            for inst, rep in targets:
                # Validate the report selection.
                cutoff_data_base = validate_report_selection(inst, rep, data_base)

                for data in cutoff_data_base:
                    # Download the reports.
                    logger.info(f'Downloading report "{rep.name}" from ' f'{inst.name} referring to "{data}"...')
                    self.pipeline.scraper(data, inst, rep)
        except IfDataScraperException as error:
            logger.exception(error.message)

        # BUG: The IF.data system generates CSV files for download in real-time,
        # using the loaded data table as the foundation.
        # Internally, it triggers the `downloadCsv` JavaScript function, which
        # constructs a Blob object of type "text/csv" and saves this file.
        # I have not been able to find a permanent solution to this issue.
        #
        # A temporary measure is to delete the empty files and rerun the
        # data scraping process, repeating this step until there are no
        # more content-less files remaining.
        self._clean_download_directory()

    def run_cleaner(self, institution: str | None = None, report: str | None = None) -> None:
        """Main function for executing the cleaner."""

        # Run the cleaner.
        targets = self._get_execution_targets(institution, report)
        for process_institution, process_report in targets:
            self.pipeline.cleaner(process_institution, process_report)

    def run_transformer(self, institution: str | None = None, report: str | None = None) -> None:
        """Main function for executing the transformer."""

        # Run the transformer for all institutions.
        targets = self._get_execution_targets(institution, report)
        for process_institution, process_report in targets:
            self.pipeline.transformer(process_institution, process_report)

    def run_loader(self, institution: str | None = None, report: str | None = None) -> None:
        """Main function for executing the loader."""

        targets = self._get_execution_targets(institution, report)

        # If no filters are provided, we can safely reset the whole database
        if not institution and not report:
            self._reset_database()

        # Run the loader.
        for loaded_institution, loaded_report in targets:
            # If a filter was applied, we only drop the specific tables we are reloading.
            if institution or report:
                table_name = f"{loaded_institution.name.lower()}_{loaded_report.name.lower()}"
                self._database_service.drop_table(table_name)

            self.pipeline.loader(loaded_institution, loaded_report)

    def run_analytics(self) -> None:
        """Executes the analytics layer (dbt) to transform Bronze data into Gold (Star Schema).

        This method triggers the dbt build command within the data_analytics directory.
        """

        logger.info('Starting analytics transformation (dbt)...')

        # Define the path to the dbt project directory, which contains the dbt models and configurations.
        dbt_project_directory = Cfg.DATA_ANALYTICS_DIRECTORY

        # Ensure the directory exists
        if not dbt_project_directory.exists():
            logger.error(f'Analytics directory not found: {dbt_project_directory}')
            raise FileNotFoundError(f'dbt project directory not found: {dbt_project_directory}')

        # Load .env files so dbt can run both from pipeline and standalone.
        project_env_file = Cfg.BASE_DIRECTORY / '.env'
        analytics_env_file = dbt_project_directory / '.env'

        # Load environment variables from both .env files,
        # with the analytics .env taking precedence if there are conflicts.
        load_dotenv(project_env_file, override=False)
        load_dotenv(analytics_env_file, override=False)

        # Set environment variables for dbt
        # Prioritize values from .env if available, otherwise use defaults from Cfg.
        silver_db_path = os.getenv('SILVER_DB_PATH') or str(Cfg.SILVER_DATABASE_FILE)
        gold_db_path = os.getenv('GOLD_DB_PATH') or str(Cfg.GOLD_DATABASE_FILE)

        # Prepare the environment variables for the subprocess call to dbt.
        env = os.environ.copy()
        env.update(
            {
                'SILVER_DB_PATH': silver_db_path,
                'GOLD_DB_PATH': gold_db_path,
                # Ensure subprocess Python uses UTF-8 consistently on Windows.
                'PYTHONUTF8': '1',
                'PYTHONIOENCODING': 'utf-8',
            }
        )

        # Remove existing Gold database to ensure a clean slate for dbt transformations.
        # We use gold_db_path (which may have been overridden by .env) instead of Cfg.GOLD_DATABASE_FILE
        # to ensure consistency between the manager and the dbt model output.
        gold_db_file = Path(gold_db_path)
        if gold_db_file.exists():
            gold_db_file.unlink()
            logger.info(f'Existing Gold database removed: {gold_db_file}')

        try:
            # Execute dbt build (runs models and tests)
            # Output streams directly to the CLI for real-time visibility
            result = subprocess.run(['uv', 'run', 'dbt', 'build'], cwd=dbt_project_directory, env=env, check=True)

            logger.info('\nAnalytics transformation completed successfully!')

        except subprocess.CalledProcessError as error:
            logger.error(f'dbt build failed with exit code {error.returncode}.')
            raise
