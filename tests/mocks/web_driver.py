"""Mocks for WebDriver interactions in tests."""

from typing import Optional

from selenium.common.exceptions import NoSuchElementException

from .element import DelayedVisibilityMockElement, MockElement


class MockWebDriver:
    """
    This class provides a simplified way to simulate interaction with a web browser
    without the need for a real browser environment. It is especially useful in unit tests
    where interaction with web elements is required.

    The class uses MockElement to simulate web elements that can be
    'clickable', 'unclickable', or 'nonexistent' to test different user interaction scenarios
    and browser behavior.
    """

    def __init__(self):
        """Initializes the MockWebDriver class."""

        self.elements: dict[str, Optional[MockElement]] = {
            'clickable': MockElement(is_displayed=True, is_enabled=True),
            'unclickable': MockElement(is_displayed=True, is_enabled=False),
            'delayed': DelayedVisibilityMockElement(is_displayed=False, is_enabled=False, delay=2),
            'nonexistent': None,
        }

    def find_element(self, by: str, value: str) -> MockElement:
        """Simulates searching for an element in the browser."""

        element = self.elements.get(value)
        if element is None:
            raise NoSuchElementException(f"Element with {by}='{value}' was not found")

        return element

    def execute_script(self, script: str, element: MockElement) -> None:
        """Simulates executing a JavaScript script.

        In the case of a click script, it calls the element's click() method.
        """

        if 'click' in script.lower():
            element.click()
