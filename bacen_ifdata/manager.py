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

from loguru import logger

from bacen_ifdata import Pipeline
from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.scraper.storage.processing import build_directory_path
from bacen_ifdata.scraper.utils import validate_report_selection
from bacen_ifdata.utilities.clean import (clean_download_base_directory,
                                          clean_empty_csv_files)
from bacen_ifdata.utilities.configurations import Config as Cfg


class PipelineManager:
    """Manages the IF.data pipeline, including scraping, cleaning, transforming, and loading data."""

    def __init__(self, pipeline: Pipeline):
        """Initializes the PipelineManager with a pipeline instance."""

        self.pipeline = pipeline

    def __clean_download_directory(self) -> None:
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
        clean_empty_csv_files(build_directory_path(
            Cfg.DOWNLOAD_DIRECTORY.value))

        # Clean up the download base directory.
        logger.info('Cleaning up the download base directory...')
        clean_download_base_directory(
            build_directory_path(Cfg.DOWNLOAD_DIRECTORY.value))

    def run_scraper(self) -> None:
        """Main function for executing the scraper."""

        try:
            # Get the available data bases.
            data_base = self.pipeline.session.get_data_bases()

            # Run the scraper...
            for institution in Institutions:
                for report in REPORTS[institution]:
                    # Validate the report selection.
                    cutoff_data_base = validate_report_selection(institution,
                                                                 report,
                                                                 data_base)

                    for data in cutoff_data_base:
                        # Download the reports.
                        logger.info(f'Downloading report "{report.name}" from '
                                    f'{institution.name} referring to "{data}"...')
                        self.pipeline.scraper(data, institution, report)
        except IfDataScraperException as error:
            logger.exception(error.message)
        finally:
            # Clean up the session, closing the browser and show report.
            if self.pipeline.session:
                self.pipeline.session.cleanup()

            # BUG: The IF.data system generates CSV files for download in real-time,
            # using the loaded data table as the foundation.
            # Internally, it triggers the `downloadCsv` JavaScript function, which
            # constructs a Blob object of type "text/csv" and saves this file.
            # I have not been able to find a permanent solution to this issue.
            #
            # A temporary measure is to delete the empty files and rerun the
            # data scraping process, repeating this step until there are no
            # more content-less files remaining.
            self.__clean_download_directory()

    def run_cleaner(self) -> None:
        """Main function for executing the cleaner."""

        # Run the cleaner.
        for process_institution in Institutions:
            for process_report in REPORTS[process_institution]:
                self.pipeline.cleaner(process_institution, process_report)

    def run_transformer(self) -> None:
        """Main function for executing the transformer."""

        # Run the transformer.
        for process_report in REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES]:
            self.pipeline.transformer(
                Institutions.PRUDENTIAL_CONGLOMERATES, process_report)

    def run_loader(self) -> None:
        """Main function for executing the loader."""

        # Run the loader.
        self.pipeline.loader(Institutions.PRUDENTIAL_CONGLOMERATES,
                             REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES])
