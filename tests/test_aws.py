"""Tests para las funciones que interactúan con AWS Cost Explorer."""
from unittest.mock import MagicMock

from monitor import get_costes, get_costes_diarios

# Respuesta simulada de Cost Explorer, con la misma estructura que la real
RESPUESTA_SIMULADA = {
    'ResultsByTime': [
        {
            'TimePeriod': {'Start': '2026-05-01', 'End': '2026-05-21'},
            'Groups': [
                {'Keys': ['AWS Lambda'], 'Metrics': {'UnblendedCost': {'Amount': '1.50'}}},
                {'Keys': ['Amazon S3'], 'Metrics': {'UnblendedCost': {'Amount': '0.30'}}},
            ],
        }
    ]
}


def test_get_costes_devuelve_lista_de_grupos():
    """get_costes debe extraer la lista de servicios de la respuesta de AWS."""
    cliente_falso = MagicMock()
    cliente_falso.get_cost_and_usage.return_value = RESPUESTA_SIMULADA

    grupos = get_costes(cliente_falso, '2026-05-01', '2026-05-21')

    assert len(grupos) == 2


def test_get_costes_extrae_nombre_de_servicio():
    """El primer grupo extraído debe ser AWS Lambda."""
    cliente_falso = MagicMock()
    cliente_falso.get_cost_and_usage.return_value = RESPUESTA_SIMULADA

    grupos = get_costes(cliente_falso, '2026-05-01', '2026-05-21')

    assert grupos[0]['Keys'][0] == 'AWS Lambda'


def test_get_costes_llama_a_cost_explorer():
    """get_costes debe llamar al método get_cost_and_usage del cliente."""
    cliente_falso = MagicMock()
    cliente_falso.get_cost_and_usage.return_value = RESPUESTA_SIMULADA

    get_costes(cliente_falso, '2026-05-01', '2026-05-21')

    cliente_falso.get_cost_and_usage.assert_called_once()


def test_get_costes_respuesta_vacia():
    """Si AWS devuelve una lista de grupos vacía, get_costes devuelve lista vacía."""
    respuesta_vacia = {
        'ResultsByTime': [
            {'TimePeriod': {'Start': '2026-05-01', 'End': '2026-05-21'}, 'Groups': []}
        ]
    }
    cliente_falso = MagicMock()
    cliente_falso.get_cost_and_usage.return_value = respuesta_vacia

    grupos = get_costes(cliente_falso, '2026-05-01', '2026-05-21')

    assert grupos == []

def test_get_costes_diarios_devuelve_lista_con_cantidad_correcta():
    """get_costes_diarios debe devolver una lista con un elemento por día."""
    respuesta_fake = {
        'ResultsByTime': [
            {'TimePeriod': {'Start': '2026-07-10', 'End': '2026-07-11'},
             'Total': {'UnblendedCost': {'Amount': '1.50', 'Unit': 'USD'}}},
            {'TimePeriod': {'Start': '2026-07-11', 'End': '2026-07-12'},
             'Total': {'UnblendedCost': {'Amount': '2.30', 'Unit': 'USD'}}},
            {'TimePeriod': {'Start': '2026-07-12', 'End': '2026-07-13'},
             'Total': {'UnblendedCost': {'Amount': '1.80', 'Unit': 'USD'}}},
        ]
    }
    cliente_falso = MagicMock()
    cliente_falso.get_cost_and_usage.return_value = respuesta_fake

    costes = get_costes_diarios(cliente_falso, dias=3)

    assert len(costes) == 3


def test_get_costes_diarios_extrae_valores_correctamente():
    """Los valores extraídos deben ser floats con los importes correctos."""
    respuesta_fake = {
        'ResultsByTime': [
            {'TimePeriod': {'Start': '2026-07-10', 'End': '2026-07-11'},
             'Total': {'UnblendedCost': {'Amount': '1.50', 'Unit': 'USD'}}},
            {'TimePeriod': {'Start': '2026-07-11', 'End': '2026-07-12'},
             'Total': {'UnblendedCost': {'Amount': '2.30', 'Unit': 'USD'}}},
        ]
    }
    cliente_falso = MagicMock()
    cliente_falso.get_cost_and_usage.return_value = respuesta_fake

    costes = get_costes_diarios(cliente_falso, dias=2)

    assert costes == [1.50, 2.30]


def test_get_costes_diarios_llama_con_granularity_daily():
    """get_costes_diarios debe pedir a AWS los datos con Granularity=DAILY y sin GroupBy."""
    respuesta_fake = {'ResultsByTime': []}
    cliente_falso = MagicMock()
    cliente_falso.get_cost_and_usage.return_value = respuesta_fake

    get_costes_diarios(cliente_falso, dias=7)

    argumentos = cliente_falso.get_cost_and_usage.call_args.kwargs
    assert argumentos['Granularity'] == 'DAILY'
    assert 'GroupBy' not in argumentos