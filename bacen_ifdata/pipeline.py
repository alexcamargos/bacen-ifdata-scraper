#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: pipeline.py
#  Version: 0.0.2
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

This script is designed to automate the download of reports from the Banco Central do Brasil's
IF.data tool. It facilitates the integration with automated data analysis and visualization tools,
ensuring easy and timely access to data.

Author: Alexsander Lopes Camargos
License: MIT
"""

from pathlib import Path
from enum import StrEnum

import pandas as pd
from loguru import logger

from bacen_ifdata.main.cleaner import main as main_cleaner
from bacen_ifdata.main.transformer import main as main_transformer
from bacen_ifdata.main.scraper import main as main_scraper
from bacen_ifdata.main.loader import DataLoaderPipeline
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import REPORTS, ReportsPrudentialConglomerates
from bacen_ifdata.scraper.session import Session
from bacen_ifdata.scraper.utils import initialize_webdriver, validate_report_selection
from bacen_ifdata.utilities.configurations import Config as Cfg


class IfDataPipeline():
    """Pipeline for the Bacen IF.data AutoScraper & Data Manager.

    This pipeline orchestrates the scraping and cleaning processes
    for the Bacen IF.data tool.

    Attributes:
        session (Session): The session object for the pipeline (initialized on demand).
    """

    def __initialize_webdriver(self):
        """Initialize the WebDriver session."""

        # Initialize the WebDriver session.
        driver = initialize_webdriver()

        # Initialize the session.
        # pylint: disable=attribute-defined-outside-init
        self.__session = Session(driver, Cfg.URL.value)

        # Open the session.
        self.__session.open()

    @property
    def session(self) -> Session:
        """Return the session object for the pipeline."""

        if not hasattr(self, '_IfDataPipeline__session'):
            self.__initialize_webdriver()

        return self.__session

    def scraper(self, _data_base: str, _institution, _report) -> None:
        """Main function for scraping the data.

        Args:
            _data_base (str): The data base to be scraped.
            _institution (str): The institution to be scraped.
            _report (str): The report to be scraped.

        Raises:
            IfDataScraperException: If an error occurs during the scraping process.
        """

        session = self.session

        # Ensure that session is initialized.
        session.open()

        # Get the available data bases.
        data_base = session.get_data_bases()

        for institution in Institutions:
            for report in REPORTS[institution]:
                # Validate the report selection.
                cutoff_data_base = validate_report_selection(institution,
                                                             report,
                                                             data_base)

                for data in cutoff_data_base:
                    # Download the reports.
                    logger.info(f'Downloading report "{report.name}" from "{institution.name}" '
                                f'referring to "{data}"...')
                    main_scraper(session, data, institution, report)

    def cleaner(self, process_institution: StrEnum, process_report: StrEnum) -> None:
        """Main process for cleaning the data.

        Args:
            process_institution (StrEnum): The institution to be processed.
            process_report (StrEnum): The report to be processed.
        """

        main_cleaner(process_institution, process_report)

    def transformer(self,
                    data_frame: pd.DataFrame,
                    institution: Institutions,
                    report: ReportsPrudentialConglomerates) -> None:
        """Main process for transforming the data.

        Args:
            data_frame (pd.DataFrame): The data frame containing the report data.
            institution (InstitutionType): The institution to be processed.
            report (Reports): The report to be processed.
        """

        main_transformer(data_frame, institution, report)

    def loader(self, data_path: Path) -> None:
        """Main process for loading the data.

        Args:
            data_path (Path): The path to the data file to be loaded.
        """

        data_loader = DataLoaderPipeline(data_path)
        data_loader.perform_data_extraction()
