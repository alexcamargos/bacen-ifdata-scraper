#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: loader.py
#  Version: 0.0.1
#
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
# ------------------------------------------------------------------------------

"""Bacen IF.data AutoScraper & Data Manager"""

from pathlib import Path
from bacen_ifdata.utilities.csv_loader import load_csv_data


# Nomes das colunas definidos com base na ordem do arquivo CSV e nas descrições do PDF.
COLUMN_NAMES = [
    # --- Identificação da Instituição ---
    "instituicao_financeira",         # Nome da instituição [cite: 1]
    # Código da instituição no cadastro do Banco Central [cite: 1]
    "codigo_instituicao",
    # Nome do conglomerado prudencial [cite: 1]
    "nome_conglomerado_prudencial",
    # Código do conglomerado financeiro [cite: 1]
    "codigo_conglomerado_financeiro",
    # Código do conglomerado prudencial [cite: 1]
    "codigo_conglomerado_prudencial",

    # --- Classificação ---
    "tcb",                            # Tipo de Consolidado Bancário [cite: 1]
    # Tipo de Controle (Público, Privado Nacional, etc.) [cite: 1]
    "tc",
    # Tipo de Instituição (Banco Múltiplo, Comercial, etc.) [cite: 1]
    "ti",

    # --- Localização e Data ---
    "cidade",                         # Cidade sede da instituição [cite: 2]
    "uf",                             # Unidade da Federação da sede [cite: 2]
    # Data-base do Relatório (MM/YYYY) [cite: 2]
    "data_base",

    # --- Dados Financeiros e Operacionais ---
    "ativo_total",                    # Valor do Ativo Total [cite: 2]
    # Valor da Carteira de Crédito Classificada [cite: 2]
    "carteira_de_credito_classificada",
    # Passivo Circulante e Exigível a Longo Prazo [cite: 2]
    "passivo_circulante_e_exigivel_lp",
    # Principal componente de Captações (Depósitos) [cite: 2]
    "captacoes_depositos",
    "patrimonio_liquido",             # Valor do Patrimônio Líquido [cite: 2]
    "lucro_liquido",                  # Valor do Lucro Líquido [cite: 2]
    # Quantidade de agências da instituição [cite: 2]
    "numero_de_agencias",
    # Quantidade de postos de atendimento [cite: 2]
    "numero_de_postos_atendimento"
]


class CsvDataLoader:
    """Lê um arquivo CSV do relatório do Banco Central e o carrega em um DataFrame Polars."""

    def __init__(self, data_path: Path):
        self.__data_path = data_path
        self.__data = None

    def __load_data(self):
        # Load data from the source
        self.__data = load_csv_data(self.__data_path.as_posix(),
                                    {
                                        'sep': ";",
                                        "header": None,
                                        "names": COLUMN_NAMES
        })

    def run(self):
        print('Loading data from:', self.__data_path.name)
        self.__load_data()

        if self.__data is None:
            raise RuntimeError("Data loading failed: self.__data is None")

        print(self.__data.sample(5))
