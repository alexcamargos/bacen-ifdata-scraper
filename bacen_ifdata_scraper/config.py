#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: config.py
#  Version: 0.0.1
#  Summary: Banco Central do Brasil IF.data Scraper
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

# URL da página onde estão os relatórios.
URL = 'https://www3.bcb.gov.br/ifdata/'

TIMEOUT = 120  # Tempo máximo de espera para carregamento de elementos.

LAST_BASE_DATE = '06/2023'  # Data-base do último relatório disponível.

# Tipo de instituição.
INSTITUTION_TYPE = 'Conglomerados Financeiros e Instituições Independentes'

REPORT_TYPE = 'Ativo'  # Tipo de relatório.
