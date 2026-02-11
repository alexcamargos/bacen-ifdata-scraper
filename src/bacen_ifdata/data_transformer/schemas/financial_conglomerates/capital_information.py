#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: capital_information.py
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

from typing import Any, Final

from bacen_ifdata.data_transformer.schemas.base_schema import BaseSchema


class FinancialConglomerateCapitalInformationSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de
    Informações de Capital de Conglomerados Financeiros,
    enriquecido com metadados do dicionário de dados.
    """

    SCHEMA_DEFINITION: Final[dict[str, dict[str, Any]]] = {
        'instituicao': {
            'description': 'Nome da instituição.',
            'type': 'text',
        },
        'codigo': {
            'description': 'Conglomerado ou CNPJ.',
            'type': 'numeric',
        },
        'consolidado_bancario': {
            'description': 'Tipo de Consolidado Bancário (TCB).',
            'type': 'categorical',
            'mapping': {
                'b1': 'Banco Comercial, Banco Múltiplo com Carteira Comercial ou Caixas Econômicas',
                'b2': 'Banco Múltiplo sem Carteira Comercial ou Banco de Câmbio ou Banco de Investimento',
                'b3s': 'Cooperativa de Crédito Singular',
                'b3c': 'Central e Confederação de Cooperativas de Crédito',
                'b4': 'Banco de Desenvolvimento',
                'n1': 'Não bancário de Crédito',
                'n2': 'Não bancário do Mercado de Capitais',
                'n4': 'Instituições de Pagamento',
            },
        },
        'segmento_resolucao': {
            'description': 'Segmento Resolução nº 4.553/2017 (SR).',
            'type': 'categorical',
            'mapping': {
                's1': (
                    'Bancos múltiplos, bancos comerciais, bancos de investimento, bancos de câmbio e caixas '
                    'econômicas que (i) tenham porte (Exposição/Produto Interno Bruto) superior a 10%; ou (ii) '
                    'exerçam atividade internacional relevante (ativos no exterior superiores a US$ 10 bilhões).'
                ),
                's2': (
                    'Composto por: (i) bancos múltiplos, bancos comerciais, bancos de investimento, '
                    'bancos de câmbio e caixas econômicas de porte inferior a 10% e igual ou superior '
                    'a 1%; e (ii) demais instituições autorizadas a funcionar pelo Banco Central do '
                    'Brasil de porte igual ou superior a 1% do PIB.'
                ),
                's3': 'Instituições de porte inferior a 1% e igual ou superior a 0,1%.',
                's4': 'Instituições de porte inferior a 0,1%.',
                's5': (
                    'Composto por: (i) instituições de porte inferior a 0,1% que utilizem metodologia '
                    'facultativa simplificada para apuração dos requerimentos mínimos de Patrimônio '
                    'de Referência (PR), de Nível I e de Capital Principal, exceto bancos múltiplos, '
                    'bancos comerciais, bancos de investimento, bancos de câmbio e caixas econômicas; '
                    'e (ii) não sujeitas a apuração de PR.'
                ),
            },
        },
        'tipo_de_consolidacao': {
            'description': 'Tipo de Consolidação (TD).',
            'type': 'categorical',
            'mapping': {
                'i': 'Instituição Independente',
                'c': 'Conglomerado',
            },
        },
        'tipo_de_controle': {
            'description': 'Tipo de Controle (TC).',
            'type': 'categorical',
            'mapping': {
                '1': 'Público',
                '2': 'Privado Nacional',
                '3': 'Privado com Controle Estrangeiro',
            },
        },
        'cidade': {'description': 'Cidade da sede da instituição.', 'type': 'text'},
        'uf': {'description': 'Estado (Unidade da Federação).', 'type': 'categorical'},
        'data_base': {'description': 'Data-base do relatório.', 'type': 'date'},
        'capital_principal_para_comparacao_com_rwa': {
            'description': 'Parcela do capital de melhor qualidade e imediatamente disponível para absorver perdas.',
            'type': 'numeric',
        },
        'capital_complementar': {
            'description': 'Instrumentos de capital e dívida perpétuos, elegíveis como patrimônio regulatório.',
            'type': 'numeric',
        },
        'patrimonio_referencia_nivel_i_para_comparacao_com_rwa': {
            'description': 'Parcela do capital formada pela soma das parcelas do Capital Principal e Capital Complementar.',
            'type': 'numeric',
        },
        'capital_nivel_ii': {
            'description': (
                'Parcela do capital composta por instrumentos subordinados, elegíveis como patrimônio '
                'regulatório, aptos a absorver perdas durante o funcionamento da instituição.'
            ),
            'type': 'numeric',
        },
        'patrimonio_referencia_para_comparacao_com_rwa': {
            'description': 'Montante de capital regulatório formado pela soma das parcelas de Capital Nível I e Capital Nível II.',
            'type': 'numeric',
        },
        'rwa_risco_credito': {
            'description': 'Parcela dos ativos ponderados pelo risco (RWA) referente à exposição ao risco de crédito.',
            'type': 'numeric',
        },
        'rwacam': {
            'description': 'Parcela do RWA referente às exposições em ouro, em moeda estrangeira e em ativos sujeitos à variação cambial.',
            'type': 'numeric',
        },
        'rwacom': {
            'description': 'Parcela do RWA referente ao risco das operações sujeitas à variação do preço de mercadorias (commodities).',
            'type': 'numeric',
        },
        'rwajur': {
            'description': 'Parcela do RWA referente às exposições sujeitas à variação de taxas de juros e cupons.',
            'type': 'numeric',
        },
        'rwaacs': {
            'description': 'Parcela do RWA referente ao risco das operações sujeitas à variação do preço de ações.',
            'type': 'numeric',
        },
        'rwa_risco_mercado': {
            'description': 'Parcela do RWA referente à exposição ao risco de mercado.',
            'type': 'numeric',
        },
        'rwa_risco_operacional': {
            'description': 'Parcela do RWA referente à exposição ao risco operacional.',
            'type': 'numeric',
        },
        'ativos_ponderados_pelo_risco_rwa': {
            'description': 'Corresponde à soma das parcelas referentes à exposição aos riscos de Crédito, de Mercado e Operacional.',
            'type': 'numeric',
        },
        'exposicao_total': {
            'description': 'Exposição Total, sem ponderação de risco, conforme definido na Circular n° 3.748 de 27 de fevereiro de 2015.',
            'type': 'numeric',
        },
        'indice_capital_principal': {
            'description': 'Relação entre Capital Principal e Ativos ponderados pelo risco.',
            'type': 'percentage',
        },
        'indice_capital_nivel_i': {
            'description': 'Relação entre o Patrimônio de Referência Nível I e os Ativos ponderados pelo risco.',
            'type': 'percentage',
        },
        'indice_basileia': {
            'description': 'Relação entre o Patrimônio de Referência e os Ativos ponderados pelo risco.',
            'type': 'percentage',
        },
        'razao_alavancagem': {
            'description': 'Relação entre o Patrimônio de Referência de Nível I e a Exposição Total.',
            'type': 'percentage',
        },
        'indice_imobilizacao': {
            'description': 'Relação entre Ativo Permanente e Patrimônio de Referência.',
            'type': 'percentage',
        },
    }
