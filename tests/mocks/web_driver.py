#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: web_driver.py
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


from selenium.common.exceptions import NoSuchElementException
from tests.mocks.element import MockElement, DelayedVisibilityMockElement


class MockWebDriver:
    """
    Essa classe provê uma maneira simplificada de simular a interação com um navegador web
    sem a necessidade de um ambiente de navegador real. É especialmente útil em testes
    unitários onde a interação com elementos da web é necessária.

    A classe utiliza MockElement para simular elementos da web que podem ser
    'clicáveis', 'não clicáveis' ou 'inexistentes' para testar diferentes cenários
    de interação do usuário e comportamento do navegador.

    Atributos:
        elements (dict): Um dicionário mapeando identificadores de elementos
                         para instâncias de MockElement ou None.

    Métodos:
        find_element(by, value): Simula a busca de um elemento no navegador.
                                 Retorna um MockElement ou None.
    """

    def __init__(self):
        self.elements = {'clickable': MockElement(is_displayed=True, is_enabled=True),
                         'unclickable': MockElement(is_displayed=True, is_enabled=False),
                         'delayed': DelayedVisibilityMockElement(is_displayed=False,
                                                                 is_enabled=False,
                                                                 delay=2),
                         'nonexistent': None}

    def find_element(self, by, value):
        element = self.elements.get(value)
        if element is None:
            raise NoSuchElementException(
                f"Elemento com {by}='{value}' não foi encontrado")
        return element
