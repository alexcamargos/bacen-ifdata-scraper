#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: cleaner.py
#  Version: 0.0.1
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

from enum import StrEnum
from pathlib import Path
from tempfile import TemporaryDirectory

from loguru import logger

from bacen_ifdata.data_cleaner.processing import normalize_csv
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.storage.collection import (
    report_inputs,
    validate_report_csv,
)
from bacen_ifdata.scraper.storage.processing import (
    build_directory_path,
    ensure_directory,
    move_artifact,
)
from bacen_ifdata.utilities.configurations import Config as Cfg


def main(institution: Institutions, report: StrEnum) -> None:
    """Normalize the validated originals for one report.

    Args:
        institution (StrEnum): The institution for which the reports will be normalized.
        report (StrEnum): The report that will be normalized.

    Returns:
        None.

    Raises:
        IfDataScraperException: The selected original has an unexpected date.
        OSError: A normalized file could not be created.
    """

    # Ensure that the processed files directory exists.
    output_directory = build_directory_path(
        Cfg.PROCESSED_FILES_DIRECTORY, institution.name.lower(), report.name.lower()
    )
    ensure_directory(output_directory)

    # Build the path to the input data directory.
    input_data_path = build_directory_path(Cfg.DOWNLOAD_DIRECTORY, institution.name.lower(), report.name.lower())

    Cfg.SCRATCH_DIRECTORY.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=Cfg.SCRATCH_DIRECTORY) as temporary:
        for period, source in sorted(report_inputs(input_data_path).items()):
            if period > Cfg.HISTORICAL_END:
                continue
            date = f'{period[5:]}/{period[:4]}'
            validate_report_csv(source, date)
            filename = f'{period}.csv'
            destination = output_directory / filename
            if destination.exists() and (
                destination.stat().st_mtime_ns >= source.stat().st_mtime_ns
            ):
                continue
            logger.info(
                f'Normalizing {institution.name}/{report.name}/{filename}.'
            )
            staged = Path(temporary) / filename
            if not normalize_csv(
                institution, report, filename,
                source=source, destination=staged,
            ):
                raise OSError(f'Could not normalize {source}.')
            move_artifact(staged, destination, replace=True)
