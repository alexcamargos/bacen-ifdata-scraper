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
from bacen_ifdata.manager import PipelineManager
from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.scraper.utils import validate_report_selection
from bacen_ifdata.utilities.version import __version__ as version
from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.data_transformer.transformers.prudential_conglomerates import PrudentialConglomeratesTransformer


def get_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: The command-line arguments parser.
    """

    # Create the parser.
    parser = argparse.ArgumentParser(
        prog='ifdata',
        description='Bacen IF.data AutoScraper & Data Manager')

    # Add the arguments.
    parser.add_argument('-s',
                        '--scraper',
                        action='store_true',
                        help='Download the reports.')

    parser.add_argument('-c',
                        '--cleaner',
                        action='store_true',
                        help='Clean the downloaded reports.')

    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version=f'%(prog)s {version}')

    parser.add_argument('-t',
                        '--transformer',
                        action='store_true',
                        help='Transform the downloaded reports.')

    parser.add_argument('-l',
                        '--loader',
                        action='store_true',
                        help='Load the processed reports.')

    return parser.parse_args()


def ifdata_scraper(scraper_pipeline: Pipeline) -> None:
    """Main function for executing the scraper."""

    try:
        # Get the available data bases.
        data_base = scraper_pipeline.session.get_data_bases()

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
                    scraper_pipeline.scraper(data, institution, report)
    except IfDataScraperException as error:
        logger.exception(error.message)
    finally:
        # Clean up the session, closing the browser and show report.
        if scraper_pipeline.session:
            scraper_pipeline.session.cleanup()

        # BUG: The IF.data system generates CSV files for download in real-time,
        # using the loaded data table as the foundation.
        # Internally, it triggers the `downloadCsv` JavaScript function, which
        # constructs a Blob object of type "text/csv" and saves this file.
        # I have not been able to find a permanent solution to this issue.
        #
        # A temporary measure is to delete the empty files and rerun the
        # data scraping process, repeating this step until there are no
        # more content-less files remaining.
        __clean_download_directory()


def ifdata_cleaner(cleaner_pipeline: Pipeline) -> None:
    """Main function for executing the cleaner."""

    # Run the cleaner.
    for process_institution in Institutions:
        for process_report in REPORTS[process_institution]:
            cleaner_pipeline.cleaner(process_institution, process_report)


def ifdata_transformer(transformer_pipeline: Pipeline) -> None:
    """Main function for executing the transformer."""

    # Run the transformer.
    for process_report in REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES]:
        transformer_pipeline.transformer(
            Institutions.PRUDENTIAL_CONGLOMERATES, process_report)


def ifdata_loader(loader_pipeline: Pipeline) -> None:
    """Main function for executing the loader."""

    # Define the path to load the data.
    loaded_institution = Institutions.INDIVIDUAL_INSTITUTIONS
    loaded_report = REPORTS[Institutions.INDIVIDUAL_INSTITUTIONS].SUMMARY

    # Run the loader.
    loader_pipeline.loader(loaded_institution, loaded_report)


def main(pipeline_manager: PipelineManager) -> None:
    """Main function to run the IF.data pipeline.

    This function orchestrates the execution of the various stages
    of the IfDataPipeline, including scraping, cleaning, transforming,
    and loading data.

    Arguments:
        pipeline_manager (PipelineManager): The pipeline manager instance to run.
    """

    # Get the arguments.
    args = get_arguments()

    logger.info('Starting the Bacen IF.data AutoScraper & Data Manager')

    # A flag to check if any specific action was requested.
    action_requested = any(
        [args.scraper, args.cleaner, args.transformer, args.loader])

    # Run the scraper.
    if args.scraper:
        logger.info('Running the scraper...')
        pipeline_manager.run_scraper()

    # Run the cleaner.
    if args.cleaner:
        logger.info('Running the cleaner...')
        pipeline_manager.run_cleaner()

    # Run the transformer.
    if args.transformer:
        logger.info('Running the transformer...')
        pipeline_manager.run_transformer()

    # Run the loader.
    if args.loader:
        logger.info('Running the loader...')
        pipeline_manager.run_loader()

    # If no specific action was requested, run the default pipeline.
    if not action_requested:
        logger.info(
            'No specific action requested, running default pipeline (cleaner and transformer)...')
        # Run the cleaner.
        pipeline_manager.run_cleaner()
        # Run the transformer.
        pipeline_manager.run_transformer()


if __name__ == '__main__':

    # Create the prudential conglomerates transformer instance.
    prudential_conglomerates_transformer = PrudentialConglomeratesTransformer()

    # Create the transformer controller instance.
    transformer_controller = TransformerController(
        prudential_conglomerates_transformer)

    # Initialize the main pipeline.
    pipeline = Pipeline(transformer_controller)

    # Create the pipeline manager instance.
    pipeline_manager = PipelineManager(pipeline)

    # Run the main pipeline.
    main(pipeline_manager)
