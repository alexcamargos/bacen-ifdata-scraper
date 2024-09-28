#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: consolidation_model.py
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


from pydantic import BaseModel, Field


# pylint: disable=missing-class-docstring
class ConsolidationType(BaseModel):
    consolidation: str = Field(
        description='Tipo de Consolidação (I) Instituição Independente, (C) Conglomerado.')
