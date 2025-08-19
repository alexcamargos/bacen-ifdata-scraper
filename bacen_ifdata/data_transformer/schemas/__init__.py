#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: __init__.py
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

import bacen_ifdata.data_transformer.schemas.prudential_conglomerate_summary as prudential_conglomerate_summary
from bacen_ifdata.data_transformer.schemas.prudential_conglomerates_assets import PrudentialConglomeratesAssetsSchema
from bacen_ifdata.data_transformer.schemas.prudential_conglomerates_liabilities import PrudentialConglomerateLiabilitiesSchema


# Instance a schema for report summary of prudential conglomerate.
PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA = prudential_conglomerate_summary.PrudentialConglomerateSummarySchema()

# Instância única para ser importada em outras partes do projeto
PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA = PrudentialConglomeratesAssetsSchema()

# Instance a schema for report liabilities of prudential conglomerate.
PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA = PrudentialConglomerateLiabilitiesSchema()


__all__ = ['PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA',
           'PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA',
           'PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA']
