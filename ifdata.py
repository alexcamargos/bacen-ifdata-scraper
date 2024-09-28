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

from bacen_ifdata import IfDataPipeline
from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.scraper.storage.processing import build_directory_path
from bacen_ifdata.scraper.utils import validate_report_selection
from bacen_ifdata.transformer.schemas.columns_names.prudential_summary import (
    COLUMN_NAMES,
)
from bacen_ifdata.utilities.clean import (
    clean_download_base_directory,
    clean_empty_csv_files,
)
from bacen_ifdata.utilities.configurations import Config as Cfg
from bacen_ifdata.utilities.csv_loader import load_csv_data
from bacen_ifdata.utilities.geographic_regions import STATE_TO_REGION as REGION
from bacen_ifdata.utilities.version import __version__ as version


def __clean_download_directory():
    """
    Performs comprehensive cleaning operations on the download directory.

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
    clean_empty_csv_files(build_directory_path(Cfg.DOWNLOAD_DIRECTORY.value))

    # Clean up the download base directory.
    logger.info('Cleaning up the download base directory...')
    clean_download_base_directory(
        build_directory_path(Cfg.DOWNLOAD_DIRECTORY.value))


def get_arguments() -> argparse.Namespace:
    """Argument parser.

    Returns:
        argparse.Namespace: The parsed arguments.
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

    return parser.parse_args()


def ifdata_scraper(scraper_pipeline: IfDataPipeline) -> None:
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
                    logger.info(f'Downloading report "{report.name}" from '
                                f'{institution.name} referring to "{data}"...')
                    scraper_pipeline.scraper(data, institution, report)
    except IfDataScraperException as error:
        logger.exception(error.message)
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


def ifdata_transformer(transformer_pipeline: IfDataPipeline) -> None:
    """Main function for executing the transformer."""

    # Define the path to load the data.
    data_path = Cfg.PROCESSED_FILES_DIRECTORY.value
    institution_type = 'prudential_conglomerates'
    report_type = 'summary'
    data_base = '2024-06.csv'
    file_path = f'{data_path}\\{institution_type}\\{report_type}\\{data_base}'

    # Configurations for correctly loading the data.
    options = {
        'sep': ';',
        'names': COLUMN_NAMES,
        'dtype': {'NumAgencias': object,
                  'NumPostosAtendimento': object}
    }
    # Load the data.
    data_frame = load_csv_data(file_path, options)

    # Create the region column based on the state column.
    position_state = data_frame.columns.get_loc('UF')
    data_frame.insert(position_state, 'Regiao', data_frame['UF'].map(REGION))

    # Run the transformer.
    transformer_pipeline.transformer(data_frame,
                                     Institutions.PRUDENTIAL_CONGLOMERATES,
                                     REPORTS[Institutions.PRUDENTIAL_CONGLOMERATES].SUMMARY)


def ifdata_cleaner(cleaner_pipeline: IfDataPipeline) -> None:
    """Main function for executing the cleaner."""

    # Run the cleaner.
    for process_institution in Institutions:
        for process_report in REPORTS[process_institution]:
            cleaner_pipeline.cleaner(process_institution, process_report)


if __name__ == '__main__':
    # Get the arguments.
    args = get_arguments()

    logger.info('Starting the Bacen IF.data AutoScraper & Data Manager')

    logger.info('Starting the Bacen IF.data AutoScraper & Data Manager')

    # Initialize the pipeline.
    pipeline = IfDataPipeline()

    if args.scraper:
        logger.info('Running only the scraper...')

        logger.info('Running only the scraper...')

        # Run the scraper.
        ifdata_scraper(pipeline)
    elif args.cleaner:
        logger.info('Running only the cleaner...')

        logger.info('Running only the cleaner...')

        # Run the cleaner.
        ifdata_cleaner(pipeline)
    elif args.transformer:
        logger.info('Running the transformer...')

        # Run the transformer.
        ifdata_transformer(pipeline)
    else:
        # Run the scraper and cleaner.
        logger.info('Running the scraper and cleaner...')

        logger.info('Running the scraper and cleaner...')

        ifdata_scraper(pipeline)
        ifdata_cleaner(pipeline)
