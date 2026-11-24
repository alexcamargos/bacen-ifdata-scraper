"""Exercise field coverage classification against IF.data CSV fixtures.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

from datetime import date
from hashlib import sha256
from pathlib import Path

import pytest

from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.data_transformer.schemas import (
    FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA,
)
from bacen_ifdata.data_transformer.transformer_factory import get_transformer
from bacen_ifdata.measure_coverage import _compare_export
from bacen_ifdata.scraper.institutions import InstitutionType
from bacen_ifdata.scraper.reports import ReportsFinancialConglomerates
from bacen_ifdata.updates import RawInput
from bacen_ifdata.utilities.configurations import Config


@pytest.mark.parametrize('matching_release', [True, False])
def test_coverage_classifies_original_values(
    tmp_path: Path, matching_release: bool,
) -> None:
    """Distinguish absent fields, null source values and mismatched counts.

    Args:
        tmp_path: Directory for the report fixture.
        matching_release: Whether Silver contains the exact Bronze input.
    Returns:
        None.
    Raises:
        OSError: The fixture cannot be written or read.
    """
    source = tmp_path / '2024-12.csv'
    original = (
        'Instituição;Código;Data;Ativo Total;Lucro Líquido;Captações;'
        'Nova;Carteira de Crédito Classificada;Número de Agências;\n'
        'Banco A;101;12/2024;1.000;NI;20;15,9;1.000;*\n'
        'Banco B;102;12/2024;2.000;NI%;40;30;2.000;2\n'
        'Total consolidado;;;3.000;;60;45,9;3.000;2\n'
    ).encode('utf-8')
    source.write_bytes(original)
    entry = RawInput(
        InstitutionType.FINANCIAL_CONGLOMERATES,
        ReportsFinancialConglomerates.SUMMARY,
        date(2024, 12, 1), source, sha256(original).hexdigest(),
        Config.URL, None,
    )
    measures = {
        'ativo_total': 2, 'lucro_liquido': 0, 'captacoes': 1,
        'patrimonio_liquido': 0, 'carteira_de_credito_classificada': None,
        'numero_de_agencias': 1,
    }
    rows = list(_compare_export(
        entry, FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA, list(measures),
        TransformerController(get_transformer),
        measures if matching_release else None,
    ))

    statuses = {row['medida']: row['situacao'] for row in rows}
    expected = {
        'ativo_total': 'coberta', 'lucro_liquido': 'sem_valores_na_origem',
        'captacoes': 'contagem_divergente',
        'patrimonio_liquido': 'sem_cabecalho_mapeado',
        'carteira_de_credito_classificada': 'medida_ausente_na_silver',
        'numero_de_agencias': 'texto_na_medida_de_origem',
    }
    if not matching_release:
        expected = dict.fromkeys(measures, 'silver_sem_mesmo_original')
    assert statuses == {**expected, None: 'coluna_numerica_sem_mapeamento'}
    assert rows[-1]['cabecalho_origem'] == 'Nova'
    assert rows[-1]['valores_origem'] == 2
    assert len({row['leiaute_sha256'] for row in rows}) == 1
