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

    def run_scraper(self) -> None:
        """Main function for executing the scraper."""

        if self.pipeline.session is None:
            raise ValueError('Session is not initialized.')

        try:
            # Get the available data bases.
            data_base: list[str] = self.pipeline.session.get_data_bases()

            # Run the scraper...
            for institution in Institutions:
                for report in REPORTS[institution]:
                    # Validate the report selection.
                    cutoff_data_base = validate_report_selection(institution, report, data_base)

                    for data in cutoff_data_base:
                        # Download the reports.
                        logger.info(
                            f'Downloading report "{report.name}" from ' f'{institution.name} referring to "{data}"...'
                        )
                        self.pipeline.scraper(data, institution, report)
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

    def run_cleaner(self) -> None:
        """Main function for executing the cleaner."""

        # Run the cleaner.
        for process_institution in Institutions:
            for process_report in REPORTS[process_institution]:
                self.pipeline.cleaner(process_institution, process_report)

    def run_transformer(self) -> None:
        """Main function for executing the transformer."""

        # Run the transformer for all institutions.
        for process_institution in Institutions:
            for process_report in REPORTS[process_institution]:
                self.pipeline.transformer(process_institution, process_report)

    def run_loader(self) -> None:
        """Main function for executing the loader."""

        # Reset the database before loading to prevent data duplication.
        self._reset_database()

        # Run the loader for all institutions.
        for loaded_institution in Institutions:
            for loaded_report in REPORTS[loaded_institution]:
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

        # Set environment variables for dbt
        env = os.environ.copy()
        env['SILVER_DB_PATH'] = str(Cfg.SILVER_DATABASE_FILE)
        env['GOLD_DB_PATH'] = str(Cfg.GOLD_DATABASE_FILE)

        # Remove existing Gold database to ensure a clean slate for dbt transformations.
        if Cfg.GOLD_DATABASE_FILE.exists():
            Cfg.GOLD_DATABASE_FILE.unlink()
            logger.info(f"Existing Gold database removed: {Cfg.GOLD_DATABASE_FILE}")

        try:
            # Execute dbt build (runs models and tests)
            # Output streams directly to the CLI for real-time visibility
            result = subprocess.run(['uv', 'run', 'dbt', 'build'], cwd=dbt_project_directory, env=env, check=True)

            logger.info('\nAnalytics transformation completed successfully!')

        except subprocess.CalledProcessError as error:
            logger.error(f'dbt build failed with exit code {error.returncode}.')
            raise
