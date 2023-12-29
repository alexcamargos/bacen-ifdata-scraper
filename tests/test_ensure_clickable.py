#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: test_ensure_clickable.py
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

import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from bacen_ifdata_scraper.utils import ensure_clickable
from tests.mocks.web_driver import MockWebDriver


@pytest.fixture
def mock_driver():
    """Retorna uma instância de MockWebDriver."""
    return MockWebDriver()


def test_ensure_clickable_clicks_when_element_is_clickable(mock_driver):
    """
    Testa se a função ensure_clickable() clica em um elemento quando ele está clicável.
    """
    ensure_clickable(mock_driver, 5, By.ID, 'clickable')
    
    assert mock_driver.elements['clickable'].is_clicked


def test_ensure_clickable_handles_timeout(mock_driver, mocker):
    """Testa se a função ensure_clickable() lida com o tempo limite."""
    mocker.patch('selenium.webdriver.support.ui.WebDriverWait.until',
                 side_effect=TimeoutException)

    with pytest.raises(TimeoutException):
        ensure_clickable(mock_driver, 10, By.ID, 'unclickable')


def test_ensure_clickable_after_delay(mock_driver, mocker):
    """
    Testa se a função ensure_clickable() aguarda até que o elemento se torne clicável.
    """

    # O elemento se torna clicável após 2 segundos.
    ensure_clickable(mock_driver, 4, By.ID, 'delayed')

    assert mock_driver.elements['delayed'].is_clicked, \
        "O elemento deveria ter sido clicado após se tornar clicável."


def test_ensure_clickable_handles_no_such_element(mock_driver, mocker):
    """Testa se a função ensure_clickable() lida com a exceção NoSuchElementException."""
    mocker.patch('selenium.webdriver.support.ui.WebDriverWait.until',
                 side_effect=lambda element: mock_driver.find_element(By.ID, element))

    with pytest.raises(NoSuchElementException):
        ensure_clickable(mock_driver, 10, By.ID, 'nonexistent')
