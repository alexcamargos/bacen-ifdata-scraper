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

from typing import Optional

from .exception import ElementNotClickableException


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

    def __init__(
        self,
        is_displayed: bool = True,
        is_enabled: bool = True,
        is_selected: bool = False,
        text: str = 'lore ipsum',
        attributes: Optional[dict[str, str]] = None,
    ):
        self._is_displayed = is_displayed
        self._is_enabled = is_enabled
        self._is_selected = is_selected
        self._text = text
        self._attributes = attributes or {}

        self.is_clicked = False

    def click(self):
        """Simula a ação de clicar no elemento. Atualiza 'is_clicked' para True."""

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

    def make_visible(self):
        """Tornar o elemento visível imediatamente."""

        self._is_displayed = True

    def get_attribute(self, attribute_name: str):
        """Retorna um valor de atributo simulado baseado no nome do atributo fornecido."""

        default_attributes = {
            'class': 'some-class',
            'href': 'https://www3.bcb.gov.br/ifdata/',
        }
        return self._attributes.get(attribute_name, default_attributes.get(attribute_name, ''))

    def text(self):
        """Retorna o texto do elemento."""

        return self._text


class DelayedVisibilityMockElement(MockElement):
    """Uma extensão de MockElement que simula um elemento da web cuja visibilidade e
    capacidade de interação são retardadas não por tempo, mas por tentativas de acesso.
    Isso permite testar mecanismos de espera (wait) de forma determinística e rápida.

    Atributos:
        required_attempts (int): O número de verificações necessárias antes
                                 que o elemento se torne visível.
    """

    def __init__(self, delay: int = 2, **kwargs):
        # Nota: 'delay' aqui é reinterpretado como número de chamadas (polls)
        # para manter compatibilidade com a assinatura existente, mas sem usar time.sleep.
        super().__init__(**kwargs)
        self._attempts = 0
        self._required_attempts = delay

    def is_displayed(self):
        """Simula a visibilidade atrasada baseada no número de chamadas."""
        if self._attempts < self._required_attempts:
            self._attempts += 1
            return False

        self._is_enabled = True
        self._is_displayed = True
        return True
