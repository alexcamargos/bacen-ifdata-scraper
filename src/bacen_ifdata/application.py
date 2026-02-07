#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: application.py
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
Application Factory for Bacen IF.data

This module provides the Application class that encapsulates the construction
of all dependencies required to run the IF.data pipeline.
"""

from types import TracebackType

from loguru import logger

from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.data_transformer.transformer_factory import get_transformer
from bacen_ifdata.interfaces import PipelineManagerProtocol, SessionProtocol
from bacen_ifdata.manager import PipelineManager
from bacen_ifdata.pipeline import Pipeline
from bacen_ifdata.scraper.interfaces.interacting import Browser
from bacen_ifdata.scraper.session import Session
from bacen_ifdata.scraper.utils import initialize_webdriver
from bacen_ifdata.utilities.configurations import Config


class Application:
    """Application factory that manages the lifecycle of all pipeline dependencies.

    This class encapsulates the construction of WebDriver, Browser, Session,
    TransformerController, Pipeline, and PipelineManager. It implements the
    context manager protocol for automatic cleanup.

    The browser/session is initialized lazily - only when the scraper is actually
    used, avoiding unnecessary resource allocation for cleaner/transformer operations.

    Usage:
        with Application(enable_cleanup=True) as app:
            app.pipeline_manager.run_transformer()  # No browser started
            app.pipeline_manager.run_scraper()       # Browser started on demand
    """

    def __init__(self, enable_cleanup: bool = True) -> None:
        """Initialize the application.

        Args:
            enable_cleanup: Whether to cleanup the session on exit. Set to False
                            for debugging purposes (keeps browser open).
        """

        self._enable_cleanup = enable_cleanup
        self._session: SessionProtocol | None = None
        self._pipeline_manager: PipelineManagerProtocol | None = None
        self._is_initialized = False

    def __enter__(self) -> 'Application':
        """Initialize the application and return the instance.

        Note: The browser/session is NOT started here. It will be lazily
        initialized when actually needed (i.e., when the scraper accesses the session).
        """

        logger.info('Initializing Bacen IF.data Application...')

        # Create transformer controller with factory.
        transformer_controller = TransformerController(get_transformer)

        # Create pipeline with session factory for lazy initialization.
        # The session is only created when scraper needs it.
        pipeline = Pipeline(transformer_controller, session_factory=self._get_session)

        self._pipeline_manager = PipelineManager(pipeline)
        self._is_initialized = True

        logger.info('Application initialized (browser will start on demand).')

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """Cleanup resources on exit.

        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Traceback if an exception occurred.

        Returns:
            False to propagate any exception that occurred.
        """

        if exc_val is not None:
            logger.error(f'An error occurred: {exc_val}')

        # Only cleanup session if it was actually initialized.
        if self._enable_cleanup and self._session is not None:
            logger.info('Finishing session...')
            self._session.cleanup()

        return False  # Don't suppress exceptions

    def _initialize_session(self) -> SessionProtocol:
        """Initialize the browser and session on demand.

        Returns:
            The initialized Session instance.
        """

        logger.info('Initializing browser session...')

        # Create browser components.
        driver = initialize_webdriver()
        browser = Browser(driver)
        session = Session(browser, Config.URL)

        # Open the session.
        session.open()

        logger.info('Browser session initialized successfully.')

        return session

    def _get_session(self) -> SessionProtocol:
        """Get or create the session instance (lazy initialization).

        Returns:
            The Session instance.
        """

        if self._session is None:
            self._session = self._initialize_session()

        return self._session

    @property
    def pipeline_manager(self) -> PipelineManagerProtocol:
        """Get the pipeline manager instance.

        Returns:
            The PipelineManager instance.

        Raises:
            RuntimeError: If accessed outside of context manager.
        """

        if not self._is_initialized:
            raise RuntimeError('Application must be used as a context manager.')

        return self._pipeline_manager

    @property
    def session(self) -> SessionProtocol:
        """Get the session instance, initializing it lazily if needed.

        This property implements lazy initialization - the browser and session
        are only created when this property is first accessed.

        Returns:
            The Session instance.

        Raises:
            RuntimeError: If accessed outside of context manager.
        """

        if not self._is_initialized:
            raise RuntimeError('Application must be used as a context manager.')

        return self._get_session()
