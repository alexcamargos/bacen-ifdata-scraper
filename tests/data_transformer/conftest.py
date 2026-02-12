"""This conftest.py file is used to automatically apply the 'transformation' marker to all tests located under the
'tests/unit/data_transformer' directory, except for specific core tests.
"""

import pytest


def pytest_collection_modifyitems(items):
    """Apply the 'transformation' marker to tests physically located
    under 'tests/unit/data_transformer', EXCEPT for specific core tests.
    """

    # List of test files to exclude from the 'transformation' marker.
    excluded_files = [
        "test_controller.py",
        "test_fixtures_integrity.py",
        "test_schema_integrity.py",
    ]

    for item in items:
        # Check if the test file path contains 'data_transformer'.
        if "data_transformer" in str(item.fspath):
            # Skip marking if the file is one of the exceptions.
            if any(exc in str(item.fspath) for exc in excluded_files):
                continue

            # Add the 'transformation' marker to the test.
            item.add_marker(pytest.mark.transformation)
