"""Tests for BaseTransformer deduplication logic."""

import pandas as pd
import pytest

from bacen_ifdata.data_transformer.transformers.base import BaseTransformer


@pytest.fixture
def base_transformer():
    """Provides an instance of BaseTransformer for testing."""

    return BaseTransformer()


@pytest.mark.parametrize(
    "input_data, expected_len, deduplication_column, expected_value",
    [
        # Case: Exact duplicates
        (
            {
                'codigo': ['32016', '32016'],
                'instituicao': ['INSTITUICAO 01', 'INSTITUICAO 01'],
                'data_base': ['2010-06-01', '2010-06-01'],
                'ativo_total': [919638.0, 919638.0],
                'operacoes_de_credito': [246279.0, 246279.0],
            },
            1,
            'ativo_total',
            919638.0,
        ),
        # Case: Null row when valid counterpart exists
        (
            {
                'codigo': ['20145', '20145'],
                'instituicao': ['INSTITUICAO 02', 'INSTITUICAO 02'],
                'data_base': ['2000-03-01', '2000-03-01'],
                'ativo_total': [pd.NA, 8443931.0],
                'operacoes_de_credito': [pd.NA, 2336336.0],
            },
            1,
            'ativo_total',
            8443931.0,
        ),
        # Case: Null row when no counterpart exists
        (
            {
                'codigo': ['123'],
                'instituicao': ['INSTITUICAO 03'],
                'data_base': ['2000-03-01'],
                'ativo_total': [pd.NA],
                'operacoes_de_credito': [pd.NA],
            },
            1,
            'ativo_total',
            pd.NA,
        ),
        # Case: Different valid rows
        (
            {
                'codigo': ['1000085', '1000085'],
                'instituicao': ['INSTITUICAO 04', 'INSTITUICAO 04'],
                'data_base': ['2019-12-01', '2019-12-01'],
                'ativo_total': [100000.0, 120000.0],
                'operacoes_de_credito': [50000.0, 60000.0],
            },
            2,
            None,
            None,
        ),
    ],
    ids=[
        "exact_duplicates",
        "redundant_null_row",
        "unique_null_row",
        "distinct_valid_rows",
    ],
)
def test_deduplicate_dataset(base_transformer, input_data, expected_len, deduplication_column, expected_value):
    """Tests deduplication logic with various scenarios."""

    data_frame = pd.DataFrame(input_data)
    result = base_transformer.deduplicate_dataset(data_frame)

    assert len(result) == expected_len

    if deduplication_column:
        actual_val = result[deduplication_column].iloc[0]
        if pd.isna(expected_value):
            assert pd.isna(actual_val)
        else:
            assert actual_val == expected_value
