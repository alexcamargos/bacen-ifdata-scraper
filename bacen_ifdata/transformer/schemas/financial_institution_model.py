#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: financial_institution_model.py
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


from pydantic import BaseModel, Field, field_validator


# pylint: disable=missing-class-docstring
class FinancialInstitution(BaseModel):
    Instituicao: str = Field(
        description='Nome da instituição ou conglomerado no cadastro do Banco Central.')
    Codigo: int = Field(
        description='Código da instituição ou conglomerado no cadastro do Banco Central.')
    Cidade: str = Field(description='Cidade da sede da instituição.')
    UF: str = Field(
        description='Unidade da Federação onde fica a sede da instituição.')
    Regiao: str = Field(
        description='Região geográfica onde fica a sede da instituição.')

    @field_validator("Instituicao", mode="before")
    @classmethod
    def transform_institution_name(cls, raw_value: str) -> str:
        """Remove a parte '- Prudencial' do nome da instituição.

        Args:
            raw_value (str): Nome da instituição.

        Returns:
            str: Nome da instituição em caixa alta.
        """

        if "-" in raw_value:
            return raw_value.split("-")[0].strip()

        return raw_value

    @field_validator("Cidade", mode="before")
    @classmethod
    def transform_city_name(cls, raw_value: str) -> str:
        """Transforma o nome da cidade para iniciar com letra maiúscula.

        Args:
            raw_value (str): Nome da cidade.

        Returns:
            str: Nome da cidade em caixa alta.
        """

        return raw_value.title()
