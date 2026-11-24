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
from bacen_ifdata.measure_coverage import audit_measure_coverage
from bacen_ifdata.scraper.storage.collection import PERIOD
from bacen_ifdata.utilities.version import __version__ as version


def get_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        None.

    Returns:
        argparse.Namespace: The command-line arguments parser.

    Raises:
        SystemExit: Invalid flags or reference month were supplied.
    """

    parser = argparse.ArgumentParser(prog='ifdata', description='Bacen IF.data AutoScraper & Data Manager')

    parser.add_argument('-s', '--scraper', action='store_true', help='Download the reports.')
    parser.add_argument('-c', '--cleaner', action='store_true', help='Clean the downloaded reports.')
    parser.add_argument('-t', '--transformer', action='store_true', help='Transform the downloaded reports.')
    parser.add_argument('-l', '--loader', action='store_true', help='Load the processed reports for silver layer.')
    parser.add_argument(
        '-a', '--analytics', action='store_true', help='Run the analytics layer, create the gold layer (dbt).'
    )
    parser.add_argument(
        '-i',
        '--institution',
        type=str,
        default=None,
        help='Filter execution by institution name (e.g., PRUDENTIAL_CONGLOMERATES).',
    )
    parser.add_argument(
        '-r', '--report', type=str, default=None, help='Filter execution by report name (e.g., SUMMARY).'
    )
    parser.add_argument(
        '--data-base', metavar='YYYY-MM',
        help='Collect one published reference month.',
    )
    parser.add_argument(
        '--repair-raw',
        action='store_true',
        help='Recollect CSVs with invalid reference dates or headers.',
    )
    parser.add_argument(
        '--refresh', action='store_true',
        help='Collect the selected month again to check for revisions.',
    )
    parser.add_argument(
        '--consolidate-csv', action='store_true',
        help='Combine local originals across all months by scope and report.',
    )
    parser.add_argument(
        '--update', action='store_true',
        help='Load changed reports and publish a tested warehouse release.',
    )
    parser.add_argument(
        '--audit-coverage', action='store_true',
        help='Compare original measures with the published Silver in Parquet.',
    )
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version}')
    parser.add_argument(
        '--no-cleanup',
        action='store_true',
        help='Keep the browser session open after execution (useful for debugging).',
    )

    args = parser.parse_args()
    if args.data_base and not PERIOD.fullmatch(args.data_base):
        parser.error('--data-base must be a month in YYYY-MM format')
    if args.refresh and (not args.data_base or args.repair_raw):
        parser.error('--refresh requires --data-base and excludes --repair-raw')
    if args.repair_raw or args.refresh:
        args.scraper = True
    if args.data_base and not args.scraper:
        parser.error('--data-base requires --scraper or --repair-raw')
    if args.update and any((
        args.cleaner, args.transformer, args.loader, args.analytics,
    )):
        parser.error('--update replaces the individual processing stages')
    if args.update and not args.scraper and (args.institution or args.report):
        parser.error('--institution and --report with --update filter collection')
    if args.audit_coverage and any((
        args.scraper, args.cleaner, args.transformer, args.loader,
        args.analytics, args.update, args.consolidate_csv,
    )):
        parser.error('--audit-coverage must run as a separate read-only action')
    return args


def run_pipeline(pipeline_manager: PipelineManagerProtocol, args: argparse.Namespace) -> None:
    """Execute the requested pipeline stages.

    Args:
        pipeline_manager: The pipeline manager instance.
        args: Parsed command-line arguments.

    Returns:
        None.

    Raises:
        IfDataScraperException: A requested export could not be validated.
    """

    logger.info('Starting the Bacen IF.data AutoScraper & Data Manager')

    # Mapping of arg names to their log message and runner method.
    actions: dict[str, tuple[str, Callable[..., None]]] = {
        'scraper': ('Running the scraper...', pipeline_manager.run_scraper),
        'cleaner': ('Running the cleaner...', pipeline_manager.run_cleaner),
        'transformer': ('Running the transformer...', pipeline_manager.run_transformer),
        'loader': ('Running the loader...', pipeline_manager.run_loader),
        'analytics': ('Running the analytics...', pipeline_manager.run_analytics),
    }

    # Extract filter args.
    kwargs = {}
    if getattr(args, 'institution', None):
        kwargs['institution'] = args.institution
    if getattr(args, 'report', None):
        kwargs['report'] = args.report

    if getattr(args, 'audit_coverage', False):
        audit_measure_coverage(**kwargs)
        return

    # Execute requested actions.
    action_executed = False
    for argument_name, (message, runner) in actions.items():
        if getattr(args, argument_name):
            logger.info(message)
            if argument_name == 'scraper':
                runner(
                    **kwargs,
                    data_base=getattr(args, 'data_base', None),
                    repair_raw=getattr(args, 'repair_raw', False),
                    refresh=getattr(args, 'refresh', False),
                )
            elif argument_name == 'analytics':
                runner()  # Analytics does not take filter kwargs.
            else:
                runner(**kwargs)  # pylint: disable=not-callable
            action_executed = True

    if getattr(args, 'consolidate_csv', False):
        pipeline_manager.run_csv_consolidation(**kwargs)
        action_executed = True

    if getattr(args, 'update', False):
        pipeline_manager.run_update()
        return

    # If no specific action was requested, run the default pipeline.
    if not action_executed:
        logger.info('No specific action requested, running default pipeline (cleaner and transformer)...')
        pipeline_manager.run_cleaner(**kwargs)
        pipeline_manager.run_transformer(**kwargs)


if __name__ == '__main__':
    args = get_arguments()

    with Application(enable_cleanup=not args.no_cleanup) as app:
        run_pipeline(app.pipeline_manager, args)
