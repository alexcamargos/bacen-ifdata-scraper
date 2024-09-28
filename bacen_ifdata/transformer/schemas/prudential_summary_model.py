#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: prudential_summary_model.py
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

from typing import Union

from pydantic import BaseModel, Field, field_validator


# pylint: disable=missing-class-docstring, missing-module-docstring
class PrudentialSummaryInformation(BaseModel):
    CarteiraCredito: float = Field(
        description='Carteira de Crédito Classificada.')
    PassivoExigivel: float = Field(
        description='Passivo Circulante e Exigível a Longo Prazo e Resultado de '
        'Exercícios Futuros.')
    Captacoes: float = Field(
        description='Captações de depósitos + Obrigações por Operações Compromissadas '
        '+ Recursos de Aceites Cambiais, Letras Imobiliárias e Hipotecárias, Debêntures'
        ' e Similares + Obrigações por Empréstimos e Repasses.')
    AtivoTotal: float = Field(
        description='Ativo Circulante e Realizável a Longo Prazo + Ativo Permanente.')
    PatrimonioLiquido: float = Field(
        description='Patrimônio Líquido + Contas de Resultado Credoras + Contas de '
        'Resultado Devedoras.')
    LucroLiquido: float = Field(
        description='Lucro Líquido, excluindo despesas de juros sobre capital.')
    PatrimonioReferencia: float = Field(
        description='Montante de capital regulatório formado pela soma das parcelas '
        'de Capital Nível I e Capital Nível II.')
    IndiceBasileia: float = Field(
        description='Relação entre o Patrimônio de Referência e Ativos ponderados pelo risco.')
    IndiceImobilizacao: float = Field(
        description='Relação entre Ativo Permanente e Patrimônio de Referência.')
    NumAgencias: int = Field(
        description='Número de agências incluídas as sedes.')
    NumPostosAtendimento: int = Field(
        description='Número de postos de atendimento da instituição ou conglomerado.')

    @field_validator('CarteiraCredito',
                     'PassivoExigivel',
                     'Captacoes',
                     'AtivoTotal',
                     'PatrimonioLiquido',
                     'LucroLiquido',
                     'PatrimonioReferencia',
                     'NumAgencias',
                     'NumPostosAtendimento',
                     mode='before')
    @classmethod
    def transform_number_format(cls, raw_value: str) -> Union[str, int]:
        """Transforma o formato de número de string para float.

        Args:
            raw_value (str): Valor em formato de string.

        Returns:
            str: Valor em formato de float.
        """

        if isinstance(raw_value, str):
            if any(substring in raw_value for substring in ['NA', 'NI']):
                return 0

            return raw_value.replace('.', '').replace(',', '.')

        return raw_value

    @field_validator('CarteiraCredito',
                     'PassivoExigivel',
                     'Captacoes',
                     'AtivoTotal',
                     'PatrimonioLiquido',
                     'LucroLiquido',
                     'PatrimonioReferencia',
                     mode='after')
    @classmethod
    def transform_value_to_millions(cls, value: float) -> float:
        """Transforma o valor de milhares para milhões.

        Args:
            value (float): Valor em milhares.

        Returns:
            float: Valor em milhões.
        """

        return value / 1_000

    @field_validator('IndiceBasileia',
                     'IndiceImobilizacao',
                     mode='before')
    @classmethod
    def transform_percentage_format(cls, raw_value: str) -> Union[str, int]:
        """
        Transforma o formato de porcentagem de string para float.

        Args:
            raw_value (str): Valor em formato de string.

        Returns:
            str: Valor em formato de float.
        """

        if isinstance(raw_value, str):
            if any(substring in raw_value for substring in ['NA', 'NI']):
                return 0

            return raw_value.replace('%', '').replace('.', '').replace(',', '.')

        return raw_value
