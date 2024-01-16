#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: run.py
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

"""Bacen IF.data AutoScraper & Data Manager"""

from enum import StrEnum

import bacen_ifdata.config as CONFIG

from bacen_ifdata.scraper.storage.processing import (build_directory_path)


def normalize_csv(institution: StrEnum, report: StrEnum, file: str) -> bool:
    """Normalizes a CSV file by removing the first line and the last two lines."""

    # Diretório onde os arquivos CSV baixados são armazenados.
    input_path = build_directory_path(CONFIG.DOWNLOAD_DIRECTORY,
                                      institution.name.lower(),
                                      report.name.lower())

    # Diretório onde os arquivos CSV normalizados serão armazenados.
    output_path = build_directory_path(CONFIG.PROCESSED_FILES_DIRECTORY,
                                       institution.name.lower(),
                                       report.name.lower())

    try:
        with open(f'{input_path}\\{file}', 'r', encoding='utf-8') as input_file, \
                open(f'{output_path}\\{file}', 'w', encoding='utf-8') as output_file:
            data = input_file.readlines()

            # Os arquivos CSV do Bacen às vezes têm uma última coluna
            # vazia no cabeçalho. Para garantir a consistência dos dados,
            # essa coluna sem conteúdo será identificada e removida.
            header = data[0].split(';')
            if header[-1] == '\n':
                # Removendo a última coluna do cabeçalho.
                header.pop()

            # Para facilitar a análise dos dados, a primeira linha do arquivo,
            # que contem o cabeçalho, será removida.
            data.pop(0)

            # Os arquivos CSV do Bacen contêm linhas extras no final com informações
            # consolidadas sobre o relatório. Estas linhas não seguem o formato
            # padrão e precisam ser removidas para uma análise correta dos dados.
            # A estratégia é identificar e descartar todas as linhas a partir da primeira
            # que não corresponde ao tamanho do cabeçalho.
            for index, line in enumerate(data):
                if len(line.rstrip().split(';')) != len(header):
                    data = data[:index]
                    # Encontramos a primeira linha que não corresponde ao tamanho do cabeçalho.
                    # Portanto, podemos o loop.
                    break

            # Salvando o conteúdo no arquivo normalizado.
            output_file.writelines(data)
        return True
    except FileNotFoundError as error:
        print(f'File not found: {error.filename}')
        return False
    except IOError as error:
        print(f'Input/output error: {error}\nFile: {error.filename}')
        return False
