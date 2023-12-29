#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: element.py
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

import time
import threading

from tests.mocks.exception import ElementNotClickableException


class MockElement:
    """
    Esta classe fornece uma maneira de simular o comportamento e as propriedades de elementos
    da web sem a necessidade de um navegador real ou interação com a web para fins de teste.

    Atributos:
        _is_displayed (bool): Indica se o elemento está visível.
        _is_enabled (bool): Indica se o elemento está habilitado.
        _is_selected (bool): Indica se o elemento está selecionado (útil para checkboxes e opções).
        is_clicked (bool): Indica se o elemento foi clicado.
        _text (str): Simula o texto associado ao elemento.

    """

    def __init__(self, is_displayed=True, is_enabled=True, is_selected=False, text='lore ipsum'):
        self._is_displayed = is_displayed
        self._is_enabled = is_enabled
        self._is_selected = is_selected
        self._text = text

        self.is_clicked = False

    def click(self):
        """
        Simula a ação de clicar no elemento. Atualiza 'is_clicked' para True.
        """
        if not self._is_displayed or not self._is_enabled:
            raise ElementNotClickableException

        self.is_clicked = True

    def is_displayed(self):
        """Retorna se o elemento está visível."""
        return self._is_displayed

    def is_enabled(self):
        """Retorna se o elemento está habilitado."""
        return self._is_enabled

    def is_selected(self):
        """Retorna se o elemento está selecionado."""
        return self._is_selected

    def make_visible(self, delay=10):
        """Tornar o elemento visível após um delay"""
        time.sleep(delay)
        self._is_displayed = True

    def get_attribute(self, attribute_name):
        """Retorna um valor de atributo simulado baseado no nome do atributo fornecido."""
        attributes = {'class': 'some-class',
                      'href': 'https://www3.bcb.gov.br/ifdata/',
                      # Adicione outros atributos conforme necessário
                      }
        return attributes.get(attribute_name, '')

    def text(self):
        """Retorna o texto do elemento."""
        return self._text


class DelayedVisibilityMockElement(MockElement):
    """
    Uma extensão de MockElement que simula um elemento da web cuja visibilidade e
    capacidade de interação são retardadas por um período especificado. A classe
    utiliza multithreading para introduzir um atraso antes de alterar o estado
    do elemento para visível e habilitado.

    Atributos:
        delay (int ou float): O tempo, em segundos, que o elemento levará
                              para se tornar visível e habilitado.
    """

    def __init__(self, is_displayed, is_enabled, delay=2):
        super().__init__(is_displayed=is_displayed, is_enabled=is_enabled)
        self.delay = delay
        threading.Thread(target=self.make_visible_after_delay).start()

    def make_visible_after_delay(self):
        """
        Um método que é executado em uma thread separada para simular
        o atraso e depois alterar os atributos de visibilidade
        e habilitação do elemento.
        """
        time.sleep(self.delay)
        self._is_displayed = True
        self._is_enabled = True
