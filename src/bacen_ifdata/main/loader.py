#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: main.py
#  Version: 0.0.1
#
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
# ------------------------------------------------------------------------------

"""
Bacen IF.data AutoScraper & Data Manager

This script is designed to automate the download of reports from the Banco Central do Brasil's
IF.data tool. It facilitates the integration with automated data analysis and visualization tools,
ensuring easy and timely access to data.

Author: Alexsander Lopes Camargos
License: MIT
"""

from contextlib import nullcontext
from datetime import date
from enum import StrEnum

from loguru import logger

from bacen_ifdata.data_loader.controller import LoaderController
from bacen_ifdata.data_loader.storage import DatabaseService
from bacen_ifdata.data_transformer.schemas.mapper import SCHEMA_BY_INSTITUTION_AND_REPORT
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.storage.collection import PERIOD
from bacen_ifdata.scraper.storage.processing import build_directory_path
from bacen_ifdata.utilities.configurations import Config as Cfg


def main(
    institution: Institutions,
    report: StrEnum,
    *,
    database_service: DatabaseService | None = None,
) -> None:
    """Load one report's historical files with period validation.

    Args:
        institution (Institutions): The institution for which the reports will be loaded.
        report (StrEnum): The report that will be loaded.
        database_service: An open service in the caller's transaction, if any.

    Returns:
        None.

    Raises:
        ValueError: A file has an invalid name, report header or period.
        OSError: A CSV file cannot be read.
        duckdb.Error: DuckDB cannot load the report.
    """

    # Check if we have schemas for this institution.
    if institution not in SCHEMA_BY_INSTITUTION_AND_REPORT:
        logger.warning(f'No schema mapping found for institution: {institution.name}. Skipping loading.')
        return

    # Get the schema for the report.
    schema_by_report = SCHEMA_BY_INSTITUTION_AND_REPORT[institution]
    report_schema = schema_by_report.get(report)
    if report_schema is None:
        logger.warning(f'No schema found for report: {report.name} in {institution.name}. Skipping.')
        return

    # Build the path to the input data directory.
    input_data_path = build_directory_path(
        Cfg.TRANSFORMED_FILES_DIRECTORY, institution.name.lower(), report.name.lower()
    )
    database = database_service or DatabaseService()
    controller = LoaderController(database)
    transaction = (
        nullcontext() if database_service is not None
        else database.transaction()
    )
    try:
        with transaction:
            for file in sorted(input_data_path.glob('*.csv')):
                month = file.stem
                if not PERIOD.fullmatch(month):
                    raise ValueError(
                        f'{file}: expected a YYYY-MM.csv filename.'
                    )
                if month > Cfg.HISTORICAL_END:
                    logger.warning(
                        f'Skipping {file}: historical window ends at '
                        f'{Cfg.HISTORICAL_END}.'
                    )
                    continue
                controller.load_report(
                    institution, report, file, report_schema,
                    period=date.fromisoformat(f'{month}-01'),
                )
    finally:
        if database_service is None:
            database.close()
