"""Tests for the integrity of all data transformation schemas in the project."""

import importlib
import inspect
import pkgutil

import pytest

import bacen_ifdata.data_transformer.schemas
from bacen_ifdata.data_transformer.controller import TransformationType
from bacen_ifdata.data_transformer.schemas.base_schema import BaseSchema


def _discover_schemas():
    """Automatically discovers all Schema classes in the project."""

    found_schemas = []
    package = bacen_ifdata.data_transformer.schemas
    path = package.__path__
    prefix = package.__name__ + "."

    for _, name, _ in pkgutil.walk_packages(path, prefix):
        try:
            module = importlib.import_module(name)
        except ImportError:
            continue

        for _, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, BaseSchema)
                and obj is not BaseSchema
                and obj.__module__ == name
            ):
                found_schemas.append(obj)

    return found_schemas


# List of schema classes discovered dynamically
SCHEMAS_TO_TEST = _discover_schemas()


@pytest.mark.parametrize("schema_class", SCHEMAS_TO_TEST)
def test_schema_general_integrity(schema_class):
    """Ensures that all schemas follow the base contract and have valid types."""

    schema = schema_class()

    # 1. The schema must have defined columns
    assert schema.column_names, f"{schema_class.__name__} has no defined columns."

    # 2. All columns must have a valid transformation type (from the Enum)
    for col in schema.column_names:
        col_type = schema.get_type(col)
        assert (
            isinstance(col_type, TransformationType) or col_type in TransformationType
        ), f"The column '{col}' in schema {schema_class.__name__} has an invalid type: {col_type}"

        # 3. All columns must have a filled description
        # Access the column definition directly in the SCHEMA_DEFINITION dictionary of the class
        col_def = schema_class.SCHEMA_DEFINITION.get(col)
        assert col_def is not None, f"Definition not found for column '{col}' in {schema_class.__name__}"

        description = col_def.get('description')
        assert (
            isinstance(description, str) and description.strip()
        ), f"The column '{col}' in schema {schema_class.__name__} must have a valid and filled description."
