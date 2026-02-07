#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: pipeline.py
#  Version: 0.0.3
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

from collections.abc import Callable
from enum import StrEnum

from bacen_ifdata.data_transformer.interfaces.controller import TransformerControllerInterface
from bacen_ifdata.interfaces import SessionProtocol
from bacen_ifdata.main.cleaner import main as main_cleaner
from bacen_ifdata.main.loader import main as main_loader
from bacen_ifdata.main.scraper import main as main_scraper
from bacen_ifdata.main.transformer import main as main_transformer
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions

# Type alias for session factory callable.
SessionFactory = Callable[[], SessionProtocol]


class Pipeline:
    """Pipeline for the Bacen IF.data AutoScraper & Data Manager.

    This pipeline orchestrates the scraping and cleaning processes
    for the Bacen IF.data tool.

    The session is lazily initialized - only created when the scraper is used.

    Attributes:
        transformer_controller: The controller for data transformation.
        session_factory: Callable that creates a session on demand.
    """

    def __init__(
        self,
        transformer_controller: TransformerControllerInterface,
        session_factory: SessionFactory | None = None,
    ) -> None:
        """Initialize the pipeline.

        Args:
            transformer_controller: The transformer controller instance.
            session_factory: Callable that creates a session on demand.
                Only needed if scraper will be used.
        """

        self.transformer_controller = transformer_controller
        self._session_factory = session_factory
        self._session: SessionProtocol | None = None

    @property
    def session(self) -> SessionProtocol | None:
        """Get the session, initializing lazily if needed.

        Returns:
            The session instance, or None if no session factory was provided.
        """

        if self._session is None and self._session_factory is not None:
            self._session = self._session_factory()

        return self._session

    def scraper(self, data_base: str, institution: Institutions, report: StrEnum) -> None:
        """Main function for scraping the data.

        Args:
            data_base (str): The data base to be scraped.
            institution (Institutions): The institution to be scraped.
            report (StrEnum): The report to be scraped.
        """

        if self.session is None:
            raise ValueError('Session is required for scraping. Provide a session_factory.')

        # Download the reports.
        main_scraper(self.session, data_base, institution, report)

    def cleaner(self, process_institution: Institutions, process_report: StrEnum) -> None:
        """Main process for cleaning the data.

        Args:
            process_institution (Institutions): The institution to be processed.
            process_report (StrEnum): The report to be processed.
        """

        main_cleaner(process_institution, process_report)

    def transformer(self, transformer_institution: Institutions, transformer_report: StrEnum) -> None:
        """Main process for transforming the data.

        Args:
            transformer_institution (Institutions): The institution to be processed.
            transformer_report (StrEnum): The report to be processed.
        """

        main_transformer(self.transformer_controller, transformer_institution, transformer_report)

    def loader(self, loaded_institution: Institutions, loaded_report: StrEnum) -> None:
        """Main process for loading the data.

        Args:
            loaded_institution (Institutions): The institution to be loaded.
            loaded_report (StrEnum): The report to be loaded.
        """

        main_loader(loaded_institution, loaded_report)
