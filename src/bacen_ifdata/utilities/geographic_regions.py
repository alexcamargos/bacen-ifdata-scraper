#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: geographic_regions.py
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
"""

from enum import StrEnum
from typing import Final


class Region(StrEnum):
    """Defines the geographic regions of Brazil.

    Attributes:
        NORTE (str): North region.
        NORDESTE (str): Northeast region.
        SUL (str): South region.
        SUDESTE (str): Southeast region.
        CENTRO_OESTE (str): Central-West region.
    """

    NORTE = 'Norte'
    NORDESTE = 'Nordeste'
    SUL = 'Sul'
    SUDESTE = 'Sudeste'
    CENTRO_OESTE = 'Centro-oeste'


# Definindo as regiões e estados do Brasil.
REGIONS_STATES: Final[dict[Region, list[str]]] = {
    Region.NORTE: ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
    Region.NORDESTE: ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    Region.SUL: ['PR', 'RS', 'SC'],
    Region.SUDESTE: ['ES', 'MG', 'RJ', 'SP'],
    Region.CENTRO_OESTE: ['DF', 'GO', 'MT', 'MS'],
}

# Mapeando os estados para as regiões do Brasil.
# Formato: {estado: regiao}
STATE_TO_REGION: Final[dict[str, Region]] = {
    state: region for region, states in REGIONS_STATES.items() for state in states
}


__all__ = ['STATE_TO_REGION']
