"""Tests for the Pipeline class in bacen_ifdata.pipeline."""

from unittest.mock import Mock, patch

import pytest

from bacen_ifdata.data_transformer.interfaces.controller import TransformerControllerInterface
from bacen_ifdata.interfaces import SessionProtocol
from bacen_ifdata.pipeline import Pipeline
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions


# pylint: disable=too-few-public-methods
class MockReport:
    """Enum for testing purposes, matching the expected type in pipeline methods."""

    SUMMARY = 'summary'


@pytest.fixture
def mock_transformer_controller():
    """Fixture that returns a mock TransformerController."""

    return Mock(spec=TransformerControllerInterface)


@pytest.fixture
def mock_session():
    """Fixture that returns a mock Session."""

    return Mock(spec=SessionProtocol)


@pytest.fixture
def mock_session_factory(mock_session):
    """Fixture that returns a mock session factory function."""

    return Mock(return_value=mock_session)


def test_pipeline_initialization(mock_transformer_controller):
    """Test proper initialization of the Pipeline."""

    pipeline = Pipeline(mock_transformer_controller)

    assert pipeline.transformer_controller == mock_transformer_controller
    assert pipeline._session_factory is None
    assert pipeline._session is None


def test_pipeline_session_lazy_loading(mock_transformer_controller, mock_session_factory, mock_session):
    """Test that the session is initialized lazily and memoized."""

    pipeline = Pipeline(mock_transformer_controller, mock_session_factory)

    # Should be None initially
    assert pipeline._session is None

    # First access should call the factory
    session = pipeline.session
    assert session == mock_session
    mock_session_factory.assert_called_once()

    # Second access should return the same object without calling factory again
    session_again = pipeline.session
    assert session_again == mock_session
    mock_session_factory.assert_called_once()  # Call count remains 1


def test_pipeline_session_property_none(mock_transformer_controller):
    """Test that session property returns None if no factory is provided."""

    pipeline = Pipeline(mock_transformer_controller, session_factory=None)

    assert pipeline.session is None


@patch('bacen_ifdata.pipeline.main_scraper')
def test_pipeline_scraper_success(mock_main_scraper, mock_transformer_controller, mock_session_factory, mock_session):
    """Test scraper method calls main_scraper with correct arguments."""

    pipeline = Pipeline(mock_transformer_controller, mock_session_factory)

    # Ensure session is initialized
    _ = pipeline.session

    data_base = '2023-06'
    institution = Institutions.FINANCIAL_CONGLOMERATES
    report = MockReport.SUMMARY

    pipeline.scraper(data_base, institution, report)

    mock_main_scraper.assert_called_once_with(mock_session, data_base, institution, report)


def test_pipeline_scraper_no_session_error(mock_transformer_controller):
    """Test scraper method raises ValueError if session is not available."""

    pipeline = Pipeline(mock_transformer_controller, session_factory=None)

    data_base = '2023-06'
    institution = Institutions.FINANCIAL_CONGLOMERATES
    report = MockReport.SUMMARY

    with pytest.raises(ValueError, match="Session is required for scraping"):
        pipeline.scraper(data_base, institution, report)


@patch('bacen_ifdata.pipeline.main_cleaner')
def test_pipeline_cleaner(mock_main_cleaner, mock_transformer_controller):
    """Test cleaner method calls main_cleaner with correct arguments."""

    pipeline = Pipeline(mock_transformer_controller)

    institution = Institutions.FINANCIAL_CONGLOMERATES
    report = MockReport.SUMMARY

    pipeline.cleaner(institution, report)

    mock_main_cleaner.assert_called_once_with(institution, report)


@patch('bacen_ifdata.pipeline.main_transformer')
def test_pipeline_transformer(mock_main_transformer, mock_transformer_controller):
    """Test transformer method calls main_transformer with correct arguments."""

    pipeline = Pipeline(mock_transformer_controller)

    institution = Institutions.FINANCIAL_CONGLOMERATES
    report = MockReport.SUMMARY

    pipeline.transformer(institution, report)

    mock_main_transformer.assert_called_once_with(mock_transformer_controller, institution, report)


@patch('bacen_ifdata.pipeline.main_loader')
def test_pipeline_loader(mock_main_loader, mock_transformer_controller):
    """Test loader method calls main_loader with correct arguments."""

    pipeline = Pipeline(mock_transformer_controller)

    institution = Institutions.FINANCIAL_CONGLOMERATES
    report = MockReport.SUMMARY

    pipeline.loader(institution, report)

    mock_main_loader.assert_called_once_with(institution, report)
