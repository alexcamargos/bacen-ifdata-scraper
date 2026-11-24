#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: scraper.py
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

from loguru import logger

from bacen_ifdata.interfaces import SessionProtocol
from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.storage.collection import (
    REPORT_DATE,
    publish_report,
    report_checksum,
    report_inputs,
    validate_report_csv,
)
from bacen_ifdata.utilities.configurations import Config as Cfg


def main(
    session: SessionProtocol,
    report_date: str,
    institution: Institutions,
    report: StrEnum,
    *,
    refresh: bool = False,
) -> None:
    """Collect a validated original for one IF.data report and date.

    Args:
        session (SessionProtocol): The session object for the scraper.
        report_date (str): The base date for the reports to be downloaded.
        institution (Institutions): The institution for which the reports will be downloaded.
        report: The report that will be downloaded.
        refresh: Request a new export even if a valid original exists.

    Returns:
        None.

    Raises:
        ValueError: The reference month does not use MM/YYYY format.
        IfDataScraperException: If both exports fail CSV validation.
        TimeoutError: If Firefox does not complete an export.
        OSError: If the validated export cannot be published.
    """

    if not REPORT_DATE.fullmatch(report_date):
        raise ValueError(f'Invalid reference month: {report_date}.')
    month, year = report_date.split('/')
    period = f'{year}-{month}'
    directory = (
        Cfg.DOWNLOAD_DIRECTORY / institution.name.lower() / report.name.lower()
    )
    existing = report_inputs(directory).get(period)
    if existing is not None:
        try:
            validate_report_csv(existing, report_date)
        except IfDataScraperException as error:
            logger.warning(f'Recollecting invalid original: {error}')
        else:
            if not refresh:
                logger.info(f'Validated original already available: {existing}')
                return

    for attempt in (1, 2):
        downloaded = session.download_reports(report_date, institution, report)
        try:
            validate_report_csv(downloaded, report_date)
        except IfDataScraperException as error:
            logger.warning(
                f'Attempt {attempt} for {institution.name}/{report.name}/'
                f'{period} rejected: {error}'
            )
            if attempt == 2:
                raise
        else:
            if (
                existing
                and report_checksum(existing) == report_checksum(downloaded)
            ):
                logger.info(f'Original content is unchanged: {existing}')
                return
            published = publish_report(
                downloaded, directory / period, Cfg.URL, Cfg.SCRATCH_DIRECTORY,
            )
            logger.info(f'Validated original saved to {published}')
            return
