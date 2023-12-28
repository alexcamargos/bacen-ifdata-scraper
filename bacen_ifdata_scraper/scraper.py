#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: scraper.py
#  Version: 0.0.1
#  Summary: Banco Central do Brasil IF.data Scraper
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
Este sistema foi projetado para automatizar o download dos relatórios da ferramenta
IF.data do Banco Central do Brasil. Criado para facilitar a integração com ferramentas
automatizadas de análise e visualização de dados, garantido acesso fácil e oportuno aos dados.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL da página onde estão os relatórios.
URL = 'https://www3.bcb.gov.br/ifdata/'
TIMEOUT = 120  # Tempo máximo de espera para carregamento de elementos.
LAST_BASE_DATE = '06/2023'  # Data-base do último relatório disponível.
# Tipo de instituição.
INSTITUTION_TYPE = 'Conglomerados Financeiros e Instituições Independentes'
REPORT_TYPE = 'Ativo'  # Tipo de relatório.


# Inicializa o WebDriver para o Firefox.
driver = webdriver.Firefox()

# Acesse a página onde estão os relatórios.
driver.get(URL)

# O conteúdo do btnDataBase é carregado dinamicamente,
# então precisamos forçar o inicio do carregamento.
btn_data_base = WebDriverWait(driver, TIMEOUT).until(
    EC.element_to_be_clickable((By.ID, 'btnDataBase'))
    )
btn_data_base.click()

# Garanta que o conteúdo do default_wait esteja carregado antes de prosseguir.
WebDriverWait(driver, TIMEOUT).until(
    EC.presence_of_element_located(
        (By.XPATH, f"//a[text()='{LAST_BASE_DATE}']"))
        )

# Agora, faça a seleção desejada.
data_base_opt = driver.find_element(
    By.XPATH, f"//a[text()='{LAST_BASE_DATE}']")
data_base_opt.click()

# Escolha o tipo de instituição desejado. Altere o texto para corresponder à sua escolha.
Institution_type_opt = driver.find_element(By.ID, 'btnTipoInst')
Institution_type_opt.click()

# Garanta que o conteúdo do btnTipoInst esteja carregado antes de prosseguir.
WebDriverWait(driver, TIMEOUT).until(
    EC.presence_of_element_located(
        (By.XPATH, f"//a[text()='{INSTITUTION_TYPE}']"))
        )

driver.find_element(
    By.XPATH, f"//a[text()='{INSTITUTION_TYPE}']").click()

# Escolha o tipo de relatório desejado.
report_type_opt = driver.find_element(By.ID, 'btnRelatorio')
report_type_opt.click()

# Garanta que o conteúdo do btnRelatorio esteja carregado antes de prosseguir.
WebDriverWait(driver, TIMEOUT).until(
    EC.presence_of_element_located((By.XPATH, f"//a[text()='{REPORT_TYPE}']"))
    )

driver.find_element(By.XPATH, f"//a[text()='{REPORT_TYPE}']").click()

# Aguarde a página atualizar com as informações do relatório escolhido.
# Aguarde até que o botão de data-base esteja clicável e clique nele para carregar as opções.
data_table_export_csv = WebDriverWait(driver, TIMEOUT).until(
    EC.element_to_be_clickable((By.ID, 'aExportCsv'))
    )
data_table_export_csv.click()

# Clique no botão de download do CSV.
btn_download_csv = driver.find_element(By.ID, 'aExportCsv')
btn_download_csv.click()

# TODO: Implementar checagem de termino do download.

# Feche o navegador após o download (opcional).
# driver.quit()
