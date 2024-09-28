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

# Definindo as regiões e estados do Brasil.
regions_states = {
    'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Sul': ['PR', 'RS', 'SC'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Centro-oeste': ['DF', 'GO', 'MT', 'MS']
}
# Mapeando os estados para as regiões do Brasil.
# Formato: {estado: regiao}
STATE_TO_REGION = {state: region for region, states in regions_states.items() for state in states}

__ALL__ = ['STATE_TO_REGION']
