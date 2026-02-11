#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: portfolio_legal_person_economic_activity.py
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


class PrudentialConglomeratePortfolioLegalPersonEconomicActivitySchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de
    Carteira de Pessoa Jurídica por Atividade Econômica de
    conglomerados prudenciais, enriquecido com metadados do dicionário de dados.
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
            'description': 'Tipo de Consolidado Bancário (B1, B2, B3S, B3C, B4, N1, N2, N4).',
            'type': 'categorical',
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
        'tipo_de_consolidacao': {
            'description': 'Tipo de Consolidação (I) identifica uma Instituição Independente e (C) identifica um Conglomerado.',
            'type': 'categorical',
            'mapping': {
                'i': 'Instituição Independente',
                'c': 'Conglomerado',
            },
        },
        'tipo_de_controle': {
            'description': 'Tipo de Controle.',
            'type': 'categorical',
            'mapping': {'1': 'Público', '2': 'Privado Nacional', '3': 'Controle Estrangeiro'},
        },
        'segmento_resolucao': {
            'description': 'Segmento conforme Resolução n.º 4.553/2017 (S1, S2, S3, S4, S5).',
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
        'segmento': {
            'description': 'Segmentos de instituições financeiras.',
            'type': 'categorical',
            'mapping': {
                '2': 'Banco Comercial',
                '4': 'BNDES',
                '5': 'Banco de Desenvolvimento',
                '6': 'Caixa Econômica Federal',
                '7': 'Caixa Econômica Estadual',
                '8': 'Banco Múltiplo',
                '9': 'Cooperativa de Crédito',
                '10': 'Sociedade de Crédito ao Microempreendedor',
                '11': 'Banco Múltiplo Cooperativo',
                '13': 'Banco de Investimento',
                '14': 'Sociedade de Crédito, Financiamento e Investimento',
                '15': 'Sociedade Corretora de TVM',
                '16': 'Sociedade Distribuidora de TVM',
                '19': 'Sociedade de Arrendamento Mercantil',
                '21': 'Sociedade Corretora de Câmbio',
                '25': 'Associação de Poupança e Empréstimo',
                '28': 'Banco Comercial Estrangeiro - Filial no país',
                '29': 'Companhia Hipotecária',
                '30': 'Agência de Fomento',
                '31': 'Sociedade de Crédito Imobiliário - Repassadora',
                '39': 'Banco de Câmbio',
                '41': 'Instituições de Pagamento',
                '43': 'Sociedades de Crédito Direto',
                '44': 'Sociedades de Empréstimo entre Pessoas',
                '196': 'Conglomerado de Mercado de Capitais',
                '197': 'Conglomerado Não-Bancário de Crédito',
                '198': 'Conglomerado - Bancário II',
                '199': 'Conglomerado - Bancário I',
            },
        },
        'cidade': {'description': 'Cidade da sede da instituição.', 'type': 'text'},
        'uf': {'description': 'Unidade da Federação onde fica a sede da instituição.', 'type': 'categorical'},
        'regiao': {'description': 'Região geográfica onde fica a sede da instituição.', 'type': 'categorical'},
        'data_base': {'description': 'Data-base do relatório.', 'type': 'date'},
        # TOTAL DA CARTEIRA
        'total_carteira_pessoa_juridica': {
            'description': (
                'Volume de crédito disponibilizado a pessoas jurídicas por instituições financeiras, '
                'excluindo carteiras adquiridas em cessão de crédito com retenção de risco por outra '
                'instituição financeira.'
            ),
            'type': 'numeric',
        },
        # 1. AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQUICULTURA
        'agricultura_vencido_a_partir_15_dias': {
            'description': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'agricultura_a_vencer_ate_90_dias': {
            'description': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - Operações a vencer em até 90 dias.',
            'type': 'numeric',
        },
        'agricultura_a_vencer_91_a_360_dias': {
            'description': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'agricultura_a_vencer_361_a_1080_dias': {
            'description': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'agricultura_a_vencer_1081_a_1800_dias': {
            'description': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'agricultura_a_vencer_1801_a_5400_dias': {
            'description': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'agricultura_a_vencer_acima_5400_dias': {
            'description': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'agricultura_total': {
            'description': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - Total do grupo.',
            'type': 'numeric',
        },
        # 2. INDÚSTRIAS DE TRANSFORMAÇÃO
        'industrias_transformacao_vencido_a_partir_15_dias': {
            'description': 'Indústrias de Transformação - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'industrias_transformacao_a_vencer_ate_90_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer em até 90 dias.',
            'type': 'numeric',
        },
        'industrias_transformacao_a_vencer_91_a_360_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'industrias_transformacao_a_vencer_361_a_1080_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'industrias_transformacao_a_vencer_1081_a_1800_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'industrias_transformacao_a_vencer_1801_a_5400_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'industrias_transformacao_a_vencer_acima_5400_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'industrias_transformacao_total': {
            'description': 'Indústrias de Transformação - Total do grupo.',
            'type': 'numeric',
        },
        # 3. CONSTRUÇÃO
        'construcao_vencido_a_partir_15_dias': {
            'description': 'Construção - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'construcao_a_vencer_ate_90_dias': {
            'description': 'Construção - Operações a vencer em até 90 dias.',
            'type': 'numeric',
        },
        'construcao_a_vencer_91_a_360_dias': {
            'description': 'Construção - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'construcao_a_vencer_361_a_1080_dias': {
            'description': 'Construção - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'construcao_a_vencer_1081_a_1800_dias': {
            'description': 'Construção - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'construcao_a_vencer_1801_a_5400_dias': {
            'description': 'Construção - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'construcao_a_vencer_acima_5400_dias': {
            'description': 'Construção - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'construcao_total': {
            'description': 'Construção - Total do grupo.',
            'type': 'numeric',
        },
        # 4. SERVIÇOS INDUSTRIAIS DE UTILIDADE PÚBLICA
        'servicos_industriais_vencido_a_partir_15_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'servicos_industriais_a_vencer_ate_90_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer em até 90 dias.',
            'type': 'numeric',
        },
        'servicos_industriais_a_vencer_91_a_360_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'servicos_industriais_a_vencer_361_a_1080_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'servicos_industriais_a_vencer_1081_a_1800_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'servicos_industriais_a_vencer_1801_a_5400_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'servicos_industriais_a_vencer_acima_5400_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'servicos_industriais_total': {
            'description': 'Serviços Industriais de Utilidade Pública - Total do grupo.',
            'type': 'numeric',
        },
        # 5. INDÚSTRIAS EXTRATIVAS
        'industrias_extrativas_vencido_a_partir_15_dias': {
            'description': 'Indústrias Extrativas - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'industrias_extrativas_a_vencer_ate_90_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer em até 90 dias.',
            'type': 'numeric',
        },
        'industrias_extrativas_a_vencer_91_a_360_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'industrias_extrativas_a_vencer_361_a_1080_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'industrias_extrativas_a_vencer_1081_a_1800_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'industrias_extrativas_a_vencer_1801_a_5400_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'industrias_extrativas_a_vencer_acima_5400_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'industrias_extrativas_total': {
            'description': 'Indústrias Extrativas - Total do grupo.',
            'type': 'numeric',
        },
        # 6. COMÉRCIO, REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS
        'comercio_vencido_a_partir_15_dias': {
            'description': 'Comércio, Reparação de Veículos Automotores e Motocicletas - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'comercio_a_vencer_ate_90_dias': {
            'description': 'Comércio, Reparação de Veículos Automotores e Motocicletas - Operações a vencer em até 90 dias.',
            'type': 'numeric',
        },
        'comercio_a_vencer_91_a_360_dias': {
            'description': 'Comércio, Reparação de Veículos Automotores e Motocicletas - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'comercio_a_vencer_361_a_1080_dias': {
            'description': 'Comércio, Reparação de Veículos Automotores e Motocicletas - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'comercio_a_vencer_1081_a_1800_dias': {
            'description': 'Comércio, Reparação de Veículos Automotores e Motocicletas - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'comercio_a_vencer_1801_a_5400_dias': {
            'description': 'Comércio, Reparação de Veículos Automotores e Motocicletas - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'comercio_a_vencer_acima_5400_dias': {
            'description': 'Comércio, Reparação de Veículos Automotores e Motocicletas - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'comercio_total': {
            'description': 'Comércio, Reparação de Veículos Automotores e Motocicletas - Total do grupo.',
            'type': 'numeric',
        },
        # 7. ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL
        'administracao_publica_vencido_a_partir_15_dias': {
            'description': 'Administração Pública, Defesa e Seguridade Social - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'administracao_publica_a_vencer_ate_90_dias': {
            'description': 'Administração Pública, Defesa e Seguridade Social - Operações a vencer em até 90 dias.',
            'type': 'numeric',
        },
        'administracao_publica_a_vencer_91_a_360_dias': {
            'description': 'Administração Pública, Defesa e Seguridade Social - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'administracao_publica_a_vencer_361_a_1080_dias': {
            'description': 'Administração Pública, Defesa e Seguridade Social - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'administracao_publica_a_vencer_1081_a_1800_dias': {
            'description': 'Administração Pública, Defesa e Seguridade Social - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'administracao_publica_a_vencer_1801_a_5400_dias': {
            'description': 'Administração Pública, Defesa e Seguridade Social - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'administracao_publica_a_vencer_acima_5400_dias': {
            'description': 'Administração Pública, Defesa e Seguridade Social - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'administracao_publica_total': {
            'description': 'Administração Pública, Defesa e Seguridade Social - Total do grupo.',
            'type': 'numeric',
        },
        # 8. TRANSPORTE, ARMAZENAGEM E CORREIO
        'transporte_vencido_a_partir_15_dias': {
            'description': 'Transporte, Armazenagem e Correio - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'transporte_a_vencer_ate_90_dias': {
            'description': 'Transporte, Armazenagem e Correio - Operações a vencer em até 90 dias.',
            'type': 'numeric',
        },
        'transporte_a_vencer_91_a_360_dias': {
            'description': 'Transporte, Armazenagem e Correio - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'transporte_a_vencer_361_a_1080_dias': {
            'description': 'Transporte, Armazenagem e Correio - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'transporte_a_vencer_1081_a_1800_dias': {
            'description': 'Transporte, Armazenagem e Correio - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'transporte_a_vencer_1801_a_5400_dias': {
            'description': 'Transporte, Armazenagem e Correio - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'transporte_a_vencer_acima_5400_dias': {
            'description': 'Transporte, Armazenagem e Correio - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'transporte_total': {
            'description': 'Transporte, Armazenagem e Correio - Total do grupo.',
            'type': 'numeric',
        },
        # 9. OUTROS
        'outros_vencido_a_partir_15_dias': {
            'description': 'Outros - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'outros_a_vencer_ate_90_dias': {
            'description': 'Outros - Operações a vencer em até 90 dias.',
            'type': 'numeric',
        },
        'outros_a_vencer_91_a_360_dias': {
            'description': 'Outros - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'outros_a_vencer_361_a_1080_dias': {
            'description': 'Outros - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'outros_a_vencer_1081_a_1800_dias': {
            'description': 'Outros - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'outros_a_vencer_1801_a_5400_dias': {
            'description': 'Outros - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'outros_a_vencer_acima_5400_dias': {
            'description': 'Outros - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'outros_total': {
            'description': 'Outros - Total do grupo.',
            'type': 'numeric',
        },
        # COLUNAS FINAIS
        'atividade_nao_informada': {
            'description': 'Atividade não Informada ou não se Aplica.',
            'type': 'numeric',
        },
        'total_nao_individualizado_pessoa_juridica': {
            'description': 'Total não Individualizado Pessoa Jurídica.',
            'type': 'numeric',
        },
        'total_exterior_pessoa_juridica': {
            'description': (
                'Volume das operações de crédito realizadas por IFs brasileiras no exterior para pessoas jurídicas.'
            ),
            'type': 'numeric',
        },
    }
