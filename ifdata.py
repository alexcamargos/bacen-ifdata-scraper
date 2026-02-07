#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: ifdata.py
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

import argparse
from collections.abc import Callable

from loguru import logger

from bacen_ifdata.application import Application
from bacen_ifdata.interfaces import PipelineManagerProtocol
from bacen_ifdata.utilities.version import __version__ as version


def get_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: The command-line arguments parser.
    """

    parser = argparse.ArgumentParser(prog='ifdata', description='Bacen IF.data AutoScraper & Data Manager')

    parser.add_argument('-s', '--scraper', action='store_true', help='Download the reports.')
    parser.add_argument('-c', '--cleaner', action='store_true', help='Clean the downloaded reports.')
    parser.add_argument('-t', '--transformer', action='store_true', help='Transform the downloaded reports.')
    parser.add_argument('-l', '--loader', action='store_true', help='Load the processed reports.')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version}')
    parser.add_argument(
        '--no-cleanup',
        action='store_true',
        help='Keep the browser session open after execution (useful for debugging).',
    )

    return parser.parse_args()


def run_pipeline(pipeline_manager: PipelineManagerProtocol, args: argparse.Namespace) -> None:
    """Execute the requested pipeline stages.

    Args:
        pipeline_manager: The pipeline manager instance.
        args: Parsed command-line arguments.
    """

    logger.info('Starting the Bacen IF.data AutoScraper & Data Manager')

    # Mapping of arg names to their log message and runner method.
    actions: dict[str, tuple[str, Callable[[], None]]] = {
        'scraper': ('Running the scraper...', pipeline_manager.run_scraper),
        'cleaner': ('Running the cleaner...', pipeline_manager.run_cleaner),
        'transformer': ('Running the transformer...', pipeline_manager.run_transformer),
        'loader': ('Running the loader...', pipeline_manager.run_loader),
    }

    # Execute requested actions.
    action_executed = False
    for argument_name, (message, runner) in actions.items():
        if getattr(args, argument_name):
            logger.info(message)
            runner()  # pylint: disable=not-callable
            action_executed = True

    # If no specific action was requested, run the default pipeline.
    if not action_executed:
        logger.info('No specific action requested, running default pipeline (cleaner and transformer)...')
        pipeline_manager.run_cleaner()
        pipeline_manager.run_transformer()


if __name__ == '__main__':
    args = get_arguments()

    with Application(enable_cleanup=not args.no_cleanup) as app:
        run_pipeline(app.pipeline_manager, args)
