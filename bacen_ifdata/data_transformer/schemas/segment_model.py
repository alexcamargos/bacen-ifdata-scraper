#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: segment_model.py
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

import math

from pydantic import BaseModel, Field, field_validator


# pylint: disable=missing-class-docstring, missing-function-docstring
class SegmentClassification(BaseModel):
    segment: str = Field(description='Segmento conforme Resolução n.º 4.553/2017.')

    @field_validator('segment', mode='before')
    @classmethod
    def validade_segment_classification(cls, value):
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return 'Não informado'

        return value
