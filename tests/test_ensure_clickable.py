"""Tests for the ensure_clickable function in the scraper utils module."""

import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from bacen_ifdata.scraper.utils import ensure_clickable
from tests.mocks.web_driver import MockWebDriver


@pytest.fixture
def mock_driver():
    """Returns an instance of MockWebDriver."""

    return MockWebDriver()


def test_ensure_clickable_clicks_when_element_is_clickable(mock_driver):
    """Tests if the ensure_clickable() function clicks an element when it is clickable."""

    ensure_clickable(mock_driver, 5, By.ID, 'clickable')

    assert mock_driver.elements['clickable'].is_clicked


def test_ensure_clickable_handles_timeout(mock_driver, mocker):
    """Tests if the ensure_clickable() function handles timeout."""

    mocker.patch('selenium.webdriver.support.ui.WebDriverWait.until', side_effect=TimeoutException)

    with pytest.raises(TimeoutException):
        ensure_clickable(mock_driver, 10, By.ID, 'unclickable')


def test_ensure_clickable_after_delay(mock_driver, mocker):
    """Tests if the ensure_clickable() function waits until the element becomes clickable."""

    # The 'delayed' element now requires some checks (polls) before becoming visible.
    # WebDriverWait will handle these checks quickly without real sleep.
    ensure_clickable(mock_driver, 4, By.ID, 'delayed')

    assert mock_driver.elements['delayed'].is_clicked, "The element should have been clicked after becoming clickable."


def test_ensure_clickable_handles_no_such_element(mock_driver, mocker):
    """Tests if the ensure_clickable() function handles the NoSuchElementException."""

    mocker.patch(
        'selenium.webdriver.support.ui.WebDriverWait.until',
        side_effect=NoSuchElementException("Element not found (Simulated)"),
    )

    with pytest.raises(NoSuchElementException):
        ensure_clickable(mock_driver, 10, By.ID, 'nonexistent')
