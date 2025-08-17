#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: prudential_summary.py
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

# Definindo os nomes das colunas do DataFrame, conforme a descrição das colunas.
COLUMN_NAMES = [
    # Nome da instituição ou conglomerado no cadastro do Banco Central.
    'Instituicao',
    # Código da instituição ou conglomerado no cadastro do Banco Central.
    'Codigo',
    'TipoConsBancario',  # Tipo de Consolidado Bancário.
    'Segmento',  # Segmento conforme Resolução n.º 4.553/2017.
    # Tipo de Consolidação (I) Instituição Independente, (C) Conglomerado.
    'TipoConsolidacao',
    # Tipo de Controle (1) Público, (2) Privado Nacional, (3) Controle Estrangeiro.
    'TipoControle',
    'Cidade',  # # Cidade da sede da instituição.
    'UF',  # Unidade da Federação onde fica a sede da instituição.
    'DataBase',  # Data-base do relatório.
    # Ativo Circulante e Realizável a Longo Prazo + Ativo Permanente.
    'AtivoTotal',
    'CarteiraCredito',  # Carteira de Crédito Classificada.
    # Passivo Circulante e Exigível a Longo Prazo e Resultado de Exercícios Futuros.
    'PassivoExigivel',
    'Captacoes',  # Captações de depósitos + Obrigações por Operações Compromissadas
    # + Recursos de Aceites Cambiais, Letras Imobiliárias e Hipotecárias,
    # Debêntures e Similares + Obrigações por Empréstimos e Repasses.
    'PatrimonioLiquido',  # Patrimônio Líquido + Contas de Resultado Credoras
    # + Contas de Resultado Devedoras.
    # Lucro Líquido, excluindo despesas de juros sobre capital.
    'LucroLiquido',
    'PatrimonioReferencia',  # Montante de capital regulatório formado pela soma
    # das parcelas de Capital Nível I e Capital Nível II.
    # Relação entre o Patrimônio de Referência e Ativos ponderados pelo risco.
    'IndiceBasileia',
    # Relação entre Ativo Permanente e Patrimônio de Referência.
    'IndiceImobilizacao',
    'NumAgencias',  # Número de agências incluídas as sedes
    'NumPostosAtendimento'  # Número de postos de atendimento da instituição ou conglomerado
]
