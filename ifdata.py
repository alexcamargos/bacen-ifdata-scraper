#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: ifdata.py
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

import argparse

from loguru import logger

from bacen_ifdata import Pipeline
from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.data_transformer.transformers.prudential_conglomerates import PrudentialConglomeratesTransformer
from bacen_ifdata.manager import PipelineManager
from bacen_ifdata.scraper.interfaces.interacting import Browser
from bacen_ifdata.scraper.session import Session
from bacen_ifdata.scraper.utils import initialize_webdriver
from bacen_ifdata.utilities.configurations import Config
from bacen_ifdata.utilities.version import __version__ as version


def get_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: The command-line arguments parser.
    """

    # Create the parser.
    parser = argparse.ArgumentParser(prog='ifdata', description='Bacen IF.data AutoScraper & Data Manager')

    # Add the arguments.
    parser.add_argument('-s', '--scraper', action='store_true', help='Download the reports.')

    parser.add_argument('-c', '--cleaner', action='store_true', help='Clean the downloaded reports.')

    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version}')

    parser.add_argument('-t', '--transformer', action='store_true', help='Transform the downloaded reports.')

    parser.add_argument('-l', '--loader', action='store_true', help='Load the processed reports.')

    parser.add_argument(
        '--no-cleanup',
        action='store_true',
        help='Keep the browser session open after execution (useful for debugging).',
    )

    return parser.parse_args()


def main(pipeline_manager: PipelineManager, enable_cleanup: bool = True) -> bool:
    """Main function to run the IF.data pipeline.

    This function orchestrates the execution of the various stages
    of the IfDataPipeline, including scraping, cleaning, transforming,
    and loading data.

    Args:
        pipeline_manager (PipelineManager): The pipeline manager instance to run.
        enable_cleanup (bool): Whether to enable session cleanup after execution.

    Returns:
        bool: The cleanup flag to be used by the caller.
    """

    # Get the arguments.
    arguments = get_arguments()

    logger.info('Starting the Bacen IF.data AutoScraper & Data Manager')

    # A flag to check if any specific action was requested.
    action_requested = any([arguments.scraper, arguments.cleaner, arguments.transformer, arguments.loader])

    # Run the scraper.
    if arguments.scraper:
        logger.info('Running the scraper...')
        pipeline_manager.run_scraper()

    # Run the cleaner.
    if arguments.cleaner:
        logger.info('Running the cleaner...')
        pipeline_manager.run_cleaner()

    # Run the transformer.
    if arguments.transformer:
        logger.info('Running the transformer...')
        pipeline_manager.run_transformer()

    # Run the loader.
    if arguments.loader:
        logger.info('Running the loader...')
        pipeline_manager.run_loader()

    # If no specific action was requested, run the default pipeline.
    if not action_requested:
        logger.info('No specific action requested, running default pipeline (cleaner and transformer)...')
        # Run the cleaner.
        pipeline_manager.run_cleaner()
        # Run the transformer.
        pipeline_manager.run_transformer()

    return enable_cleanup


if __name__ == '__main__':
    # Initialize the session and driver, handling context management manually for now
    # to ensure proper cleanup in case of exceptions.
    driver = initialize_webdriver()
    browser = Browser(driver)
    session = Session(browser, Config.URL.value)

    # Get command-line arguments to check cleanup flag.
    arguments = get_arguments()
    enable_session_cleanup = not arguments.no_cleanup

    try:
        # Open the session.
        session.open()

        # Create the prudential conglomerates transformer instance.
        prudential_conglomerates_transformer = PrudentialConglomeratesTransformer()

        # Create the transformer controller instance.
        transformer_controller = TransformerController(prudential_conglomerates_transformer)

        # Initialize the main pipeline with the session injected.
        pipeline = Pipeline(transformer_controller, session)

        # Create the pipeline manager instance.
        pipeline_manager = PipelineManager(pipeline)

        # Run the main pipeline.
        main(pipeline_manager, enable_session_cleanup)

    except Exception as error:
        logger.error(f"An error occurred: {error}")
        raise error
    finally:
        if enable_session_cleanup:
            logger.info("Finishing session...")
            session.cleanup()
