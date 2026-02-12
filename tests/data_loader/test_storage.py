#!/usr/bin/env python
# encoding: utf-8

"""
Unit tests for the DatabaseManager class.
"""

from pathlib import Path
from typing import Generator

import duckdb
import pytest

from bacen_ifdata.data_loader.storage import DatabaseService
from bacen_ifdata.data_transformer.schemas.base_schema import BaseSchema


# Mock Schema for testing
class MockSchema(BaseSchema):
    """Mock schema for testing purposes."""

    SCHEMA_DEFINITION = {
        'id': {'type': 'integer', 'description': 'Unique identifier'},
        'name': {'type': 'text', 'description': 'Name of the entity'},
        'value': {'type': 'numeric', 'description': 'Monetary value'},
        'percentage': {'type': 'percentage', 'description': 'Percentage value'},
        'active': {'type': 'boolean', 'description': 'Is active?'},
    }


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """Fixture to provide a temporary database path."""

    return tmp_path / "test_warehouse.duckdb"


@pytest.fixture
def database_service(db_path: Path) -> Generator[DatabaseService, None, None]:
    """Fixture to provide a DatabaseManager instance."""

    manager = DatabaseService(db_path)
    yield manager
    manager.close()


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Fixture to create a sample CSV file."""

    csv_file = tmp_path / "data.csv"
    content = "id,name,value,percentage,active\n1,Test Entity,100.50,10.5,True\n2,Another Entity,200.00,20.0,False"
    csv_file.write_text(content, encoding='utf-8')

    return csv_file


def test_connect(database_service: DatabaseService, db_path: Path):
    """Test connection to the database."""
    conn = database_service.connection
    assert isinstance(conn, duckdb.DuckDBPyConnection)
    assert db_path.exists()


def test_create_table(database_service: DatabaseService):
    """Test table creation based on schema."""

    table_name = "test_table"
    schema = MockSchema()

    database_service.create_table(table_name, schema)

    # Verify table exists
    conn = database_service.connection
    result = conn.execute(
        "SELECT count(*) FROM information_schema.tables WHERE table_name = ?", [table_name]
    ).fetchone()
    assert result[0] == 1

    # Verify columns and types
    columns = conn.execute(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = ? ORDER BY ordinal_position",
        [table_name],
    ).fetchall()

    expected_columns = [
        ('id', 'BIGINT'),
        ('name', 'VARCHAR'),
        ('value', 'DOUBLE'),
        ('percentage', 'DOUBLE'),
        ('active', 'BOOLEAN'),
    ]

    assert columns == expected_columns


def test_insert_data(database_service: DatabaseService, sample_csv: Path):
    """Test data insertion from CSV."""

    table_name = "test_load"
    schema = MockSchema()

    database_service.create_table(table_name, schema)
    database_service.insert_data(table_name, sample_csv, schema)

    # Verify data count
    connection = database_service.connection
    count = connection.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
    assert count == 2

    # Verify content
    row = connection.execute(f"SELECT name, value, active FROM {table_name} WHERE id = 1").fetchone()
    assert row == ('Test Entity', 100.5, True)


def test_create_table_idempotency(database_service: DatabaseService):
    """Test that create_table is idempotent (can be run multiple times)."""

    table_name = "test_idempotency"
    schema = MockSchema()

    database_service.create_table(table_name, schema)
    database_service.create_table(table_name, schema)  # Should not raise error

    connection = database_service.connection
    result = connection.execute(
        "SELECT count(*) FROM information_schema.tables WHERE table_name = ?", [table_name]
    ).fetchone()
    assert result[0] == 1
