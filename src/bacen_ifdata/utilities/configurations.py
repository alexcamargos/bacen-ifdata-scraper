#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: configurations.py
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
Configuration settings for Bacen IF.data AutoScraper & Data Manager

This module contains the configuration settings for scraping IF.data reports from
Banco Central do Brasil, including URLs, timeouts, and specific report details.

Author: Alexsander Lopes Camargos
License: MIT

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

from dataclasses import dataclass
from os import getenv
from pathlib import Path
from typing import ClassVar


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class Config:
    """Configuration settings for Bacen IF.data AutoScraper & Data Manager.

    Args:
        URL: Historical IF.data report page.
        TIMEOUT: Source and browser timeout in seconds.
        BASE_DIRECTORY: Project directory.
        DATA_DIRECTORY: Root of the data layers.
        SCRATCH_DIRECTORY: Temporary workspace.
        DOWNLOAD_DIRECTORY: Root of the raw layer.
        DOWNLOAD_FILE_NAME: Filename used by the portal export.
        PROCESSED_FILES_DIRECTORY: Directory for cleaned CSVs.
        TRANSFORMED_FILES_DIRECTORY: Directory for typed CSVs.
        DATA_ANALYTICS_DIRECTORY: Directory of the dbt project.
        SILVER_DATABASE_FILE: Default Silver warehouse path.
        GOLD_DATABASE_FILE: Default Gold warehouse path.
    Returns:
        The application configuration.
    Raises:
        None.
    """

    # Historical source and its final reference month.
    URL: str = 'https://www3.bcb.gov.br/ifdata/index2024.html'
    HISTORICAL_CATALOG: ClassVar[str] = (
        'https://www3.bcb.gov.br/ifdata/rest/relatorios2000a2024'
    )
    HISTORICAL_END: ClassVar[str] = '2024-12'
    CURRENT_URL: ClassVar[str] = 'https://www3.bcb.gov.br/ifdata/'
    CURRENT_CATALOG: ClassVar[str] = (
        'https://www3.bcb.gov.br/ifdata/rest/relatorios2025a2030'
    )

    # Maximum waiting time for elements to load.
    TIMEOUT: int = 120
    BASE_DIRECTORY: Path = Path.cwd()
    DATA_DIRECTORY: Path = Path(
        getenv('IFDATA_DATA_DIRECTORY') or BASE_DIRECTORY / 'data'
    ).resolve()
    SCRATCH_DIRECTORY: Path = BASE_DIRECTORY / 'scratch'
    DOWNLOAD_DIRECTORY: Path = DATA_DIRECTORY / 'raw'
    CURRENT_INTERIM_DIRECTORY: Path = (
        DATA_DIRECTORY / 'interim' / 'ifdata_2025'
    )
    DOWNLOAD_FILE_NAME: str = 'dados.csv'
    _ISOLATED_DATA = DATA_DIRECTORY != BASE_DIRECTORY / 'data'
    PROCESSED_FILES_DIRECTORY: Path = DATA_DIRECTORY / (
        'interim/cleaned' if _ISOLATED_DATA else 'processed'
    )
    TRANSFORMED_FILES_DIRECTORY: Path = DATA_DIRECTORY / (
        'interim/typed' if _ISOLATED_DATA else 'transformed'
    )
    DATA_ANALYTICS_DIRECTORY: Path = (
        BASE_DIRECTORY / 'src' / 'bacen_ifdata' / 'data_analytics'
    )

    # Database Star Schema Architecture Paths.
    SILVER_DATABASE_FILE: Path = DATA_DIRECTORY / (
        'interim/silver_warehouse.duckdb'
        if _ISOLATED_DATA else 'silver_warehouse.duckdb'
    )
    GOLD_DATABASE_FILE: Path = DATA_DIRECTORY / (
        'processed/gold_warehouse.duckdb'
        if _ISOLATED_DATA else 'gold_warehouse.duckdb'
    )


__all__ = ['Config']
