#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: capital_information.py
#  Version: 0.0.1
#
#  Summary: Project Name
#           Quick description of the project.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

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


PR_HEADER = 'Patrimônio de Referência para Comparação com o RWA'
RWA_HEADER = 'Ativos Ponderados pelo Risco (RWA)'


class PrudentialConglomerateCapitalInformationSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de
    conglomerados prudenciais, enriquecido com metadados do dicionário de dados.
    """

    SCHEMA_DEFINITION: Final[dict[str, dict[str, Any]]] = {
        'instituicao': {
            'description': 'Nome da instituição ou conglomerado no cadastro do Banco Central.',
            'type': 'text',
            'required': True,
        },
        'codigo': {
            'description': 'Código da instituição ou conglomerado no cadastro do Banco Central.',
            'type': 'integer',
            'required': True,
        },
        'consolidado_bancario': {
            'description': 'Tipo de Consolidado Bancário (B1, B2, B3S, B3C, B4, N1, N2, N4).',
            'type': 'categorical',
            'raw_csv_header': 'TCB',
            'mapping': {
                'b1': (
                    'Instituição individual do tipo Banco Comercial, Banco Múltiplo com Carteira Comercial '
                    'ou caixas econômicas e Conglomerado composto de pelo menos uma instituição do tipo Banco '
                    'Comercial, Banco Múltiplo com Carteira Comercial ou caixas econômicas.'
                ),
                'b2': (
                    'Instituição individual do tipo Banco Múltiplo sem Carteira Comercial ou Banco de Câmbio '
                    'ou Banco de Investimento e Conglomerado composto de pelo menos uma instituição do tipo '
                    'Banco Múltiplo sem Carteira Comercial ou Banco de Investimento, mas sem conter instituições '
                    'do tipo Banco Comercial e Banco Múltiplo com Carteira Comercial.'
                ),
                'b3s': 'Cooperativa de Crédito Singular.',
                'b3c': 'Central e Confederação de Cooperativas de Crédito.',
                'b4': 'Banco de Desenvolvimento',
                'n1': 'Instituição não bancária atuante no mercado de crédito.',
                'n2': 'Instituição não bancária atuante no mercado de capitais.',
                'n4': 'Instituições de pagamento.',
            },
        },
        'segmento_resolucao': {
            'description': 'Segmento conforme Resolução n.º 4.553/2017 (S1, S2, S3, S4, S5).',
            'type': 'categorical',
            'raw_csv_header': 'SR',
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
        'tcip': {
            'description': 'Classificação das instituições conforme Resolução nº 197/2022 (Tipo 1, Tipo 2, Tipo 3).',
            'type': 'categorical',
            'mapping': {
                '1': (
                    'Tipo 1: conglomerado prudencial cuja instituição líder seja instituição financeira ou'
                    ' outra instituição autorizada a funcionar pelo Banco Central do Brasil sujeita à Lei'
                    ' nº 4.595, de 31 de dezembro de 1964.'
                ),
                '2': (
                    'Tipo 2: conglomerado prudencial cuja instituição líder seja instituição de pagamento'
                    ' e que não seja integrado por instituição financeira ou por outra instituição'
                    ' autorizada a funcionar pelo Banco Central do Brasil sujeita à Lei nº 4.595, de 1964,'
                    ' ou sujeita à Lei nº 10.194, de 14 de fevereiro de 2001.'
                ),
                '3': (
                    'Tipo 3: conglomerado prudencial cuja instituição líder seja instituição de pagamento'
                    ' e que seja integrado por instituição financeira ou por outra instituição autorizada'
                    ' a funcionar pelo Banco Central do Brasil sujeita à Lei nº 4.595, de 1964, ou sujeita'
                    ' à Lei nº 10.194, de 2001.'
                ),
                'Em branco': 'Conglomerados ou instituições que não realizem serviços de pagamento.',
            },
        },
        'tipo_de_consolidacao': {
            'description': 'Tipo de Consolidação (I) identifica uma Instituição Independente e (C) identifica um Conglomerado.',
            'type': 'categorical',
            'raw_csv_header': 'TD',
            'mapping': {
                'i': 'Instituição Independente',
                'c': 'Conglomerado',
            },
        },
        'tipo_de_controle': {
            'description': 'Tipo de Controle.',
            'type': 'categorical',
            'raw_csv_header': 'TC',
            'mapping': {'1': 'Público', '2': 'Privado Nacional', '3': 'Controle Estrangeiro'},
        },
        'cidade': {'description': 'Cidade da sede da instituição.', 'type': 'text'},
        'uf': {'description': 'Unidade da Federação onde fica a sede da instituição.', 'type': 'categorical'},
        'regiao': {'description': 'Região geográfica onde fica a sede da instituição.', 'type': 'categorical'},
        'data_base': {
            'description': 'Data-base do relatório.',
            'type': 'date',
            'required': True,
        },
        # The first column of a group keeps its group label after cleaning.
        'capital_principal_para_comparacao_com_rwa': {
            'description': 'Parcela do capital de melhor qualidade e imediatamente disponível para absorver perdas.',
            'type': 'numeric',
            'raw_csv_header': PR_HEADER,
        },
        'capital_complementar': {
            'description': 'Instrumentos de capital e dívida perpétuos, elegíveis como patrimônio regulatório.',
            'type': 'numeric',
            'raw_csv_header': f'{PR_HEADER} - Capital Complementar (b)',
        },
        'patrimonio_referencia_nivel_i_para_comparacao_com_rwa': {
            'description': 'Soma das parcelas do Capital Principal e Capital Complementar.',
            'type': 'numeric',
            'raw_csv_header': (
                f'{PR_HEADER} - Patrimônio de Referência Nível I '
                'para Comparação com RWA (c) = (a) + (b)'
            ),
        },
        'capital_nivel_ii': {
            'description': (
                'Parcela do capital composta por instrumentos subordinados, elegíveis como patrimônio '
                'regulatório, aptos a absorver perdas durante o funcionamento da instituição.'
            ),
            'type': 'numeric',
            'raw_csv_header': f'{PR_HEADER} - Capital Nível II (d)',
        },
        'patrimonio_referencia_para_comparacao_com_rwa': {
            'description': 'Montante de capital regulatório (Nível I + Nível II).',
            'type': 'numeric',
            'raw_csv_header': [
                f'{PR_HEADER} - {PR_HEADER} (e)',
                f'{PR_HEADER} - {PR_HEADER}',
            ],
        },
        'rwa_risco_credito': {
            'description': (
                'Parcela dos ativos ponderados pelo risco (RWA) referente à exposição ao risco de '
                'crédito. Segundo abordagem padronizada (RWAcpad) ou segundo modelo interno IRB (RWAcirb).'
            ),
            'type': 'numeric',
            'raw_csv_header': RWA_HEADER,
        },
        'rwacam': {
            'description': 'Parcela do RWA referente a exposições em ouro, moeda estrangeira e variação cambial.',
            'type': 'numeric',
            'raw_csv_header': f'{RWA_HEADER} - RWAcam (g1)',
        },
        'rwacom': {
            'description': 'Parcela do RWA referente ao risco de variação do preço de mercadorias (commodities).',
            'type': 'numeric',
            'raw_csv_header': f'{RWA_HEADER} - RWAcom (g2)',
        },
        'rwajur': {
            'description': 'Parcela do RWA referente a exposições sujeitas à variação de taxas de juros e cupons.',
            'type': 'numeric',
            'raw_csv_header': f'{RWA_HEADER} - RWAjur (g3)',
        },
        'rwaacs': {
            'description': 'Parcela do RWA referente ao risco de operações sujeitas à variação do preço de ações.',
            'type': 'numeric',
            'raw_csv_header': f'{RWA_HEADER} - RWAacs (g4)',
        },
        'rwacva': {
            'description': 'Parcela do RWA referente ao ajuste para derivativos por variação de qualidade creditícia (CVA).',
            'type': 'numeric',
            'raw_csv_header': f'{RWA_HEADER} - RWAcva (g5)',
        },
        'rwadrc': {
            'description': (
                'Parcela do RWA relativa às exposições ao risco de crédito dos instrumentos '
                'financeiros classificados na carteira de negociação.'
            ),
            'type': 'numeric',
            'raw_csv_header': f'{RWA_HEADER} - RWAdrc (g6)',
        },
        'rwa_risco_mercado': {
            'description': 'Parcela do RWA referente à exposição ao risco de mercado.',
            'type': 'numeric',
            'raw_csv_header': [
                f'{RWA_HEADER} - RWA para Risco de Mercado (g) = '
                '(g1) + (g2) + (g3) + (g4)',
                f'{RWA_HEADER} - RWA para Risco de Mercado (g) = '
                '(g1) + (g2) + (g3) + (g4) + (g5)',
                f'{RWA_HEADER} - RWA para Risco de Mercado (g) = '
                '(g1) + (g2) + (g3) + (g4) + (g5) + (g6)',
            ],
        },
        'rwa_risco_operacional': {
            'description': 'Parcela do RWA referente à exposição ao risco operacional.',
            'type': 'numeric',
            'raw_csv_header': f'{RWA_HEADER} - RWA para Risco Operacional (h)',
        },
        'rwasp': {
            'description': 'Parcela do RWA relativa ao cálculo de capital para riscos de serviços de pagamento.',
            'type': 'numeric',
            'raw_csv_header': f'{RWA_HEADER} - RWAsp (i)',
        },
        'ativos_ponderados_pelo_risco_rwa': {
            'description': 'Soma das parcelas de RWA para os riscos de Crédito, Mercado, Operacional e Serviço de Pagamento.',
            'type': 'numeric',
            'raw_csv_header': [
                f'{RWA_HEADER} - {RWA_HEADER} (i) = (f) + (g) + (h)',
                f'{RWA_HEADER} - {RWA_HEADER} (j) = (f) + (g) + (h) + (i)',
            ],
        },
        'exposicao_total': {
            'description': 'Exposição Total, sem ponderação de risco, conforme Circular nº 3.748/2015.',
            'type': 'numeric',
            'raw_csv_header': ['Exposição Total (j)', 'Exposição Total (k)'],
        },
        'indice_capital_principal': {
            'description': 'Relação entre o Capital Principal e os Ativos Ponderados pelo Risco (RWA).',
            'type': 'percentage',
            'raw_csv_header': [
                'Índice de Capital Principal (k) = (a) / (i)',
                'Índice de Capital Principal (l) = (a) / (j)',
            ],
        },
        'indice_capital_nivel_i': {
            'description': 'Relação entre o Patrimônio de Referência Nível I e os Ativos Ponderados pelo Risco (RWA).',
            'type': 'percentage',
            'raw_csv_header': [
                'Índice de Capital Nível I (l) = (c) / (i)',
                'Índice de Capital Nível I (m) = (c) / (j)',
            ],
        },
        'indice_basileia': {
            'description': 'Relação entre o Patrimônio de Referência e os Ativos Ponderados pelo Risco (RWA).',
            'type': 'percentage',
            'raw_csv_header': [
                'Índice de Basileia (m) = (e) / (i)',
                'Índice de Basileia (n) = (e) / (j)',
            ],
        },
        'adicional_capital_principal': {
            'description': 'Requerimento de adicional de capital principal (ACP Conservação, Contracíclico, Sistêmico).',
            'type': 'numeric',
            'raw_csv_header': [
                'Adicional de Capital Principal',
                'Adicional de Capital Principal (o)',
            ],
        },
        'razao_alavancagem': {
            'description': 'Relação entre o Patrimônio de Referência Nível I e a Exposição Total.',
            'type': 'percentage',
            'raw_csv_header': [
                'Razão de Alavancagem (n) = (c) / (j)',
                'Razão de Alavancagem (o) = (c) / (k)',
                'Razão de Alavancagem (p) = (c) / (k)',
            ],
        },
        'indice_imobilizacao': {
            'description': 'Relação entre o Ativo Permanente e o Patrimônio de Referência.',
            'type': 'percentage',
            'raw_csv_header': [
                'Índice de Imobilização (o)', 'Índice de Imobilização (p)',
                'Índice de Imobilização (q)',
            ],
        },
    }
