"""Tests para el formateo de mensajes."""
from monitor import formatear_mensaje


def test_mensaje_incluye_fechas():
    """El mensaje debe incluir las fechas de inicio y fin."""
    grupos = []
    mensaje = formatear_mensaje(grupos, '2026-05-01', '2026-05-21')

    assert '2026-05-01' in mensaje
    assert '2026-05-21' in mensaje


def test_mensaje_incluye_servicios_con_coste():
    """Los servicios con coste mayor que 0 deben aparecer en el mensaje."""
    grupos = [
        {'Keys': ['AWS Lambda'], 'Metrics': {'UnblendedCost': {'Amount': '1.50'}}},
        {'Keys': ['Amazon S3'], 'Metrics': {'UnblendedCost': {'Amount': '0.30'}}},
    ]
    mensaje = formatear_mensaje(grupos, '2026-05-01', '2026-05-21')

    assert 'AWS Lambda' in mensaje
    assert 'Amazon S3' in mensaje


def test_mensaje_omite_servicios_a_cero():
    """Los servicios con coste 0 NO deben aparecer en el mensaje."""
    grupos = [
        {'Keys': ['AWS Lambda'], 'Metrics': {'UnblendedCost': {'Amount': '0'}}},
    ]
    mensaje = formatear_mensaje(grupos, '2026-05-01', '2026-05-21')

    assert 'AWS Lambda' not in mensaje


def test_mensaje_calcula_total():
    """El mensaje debe incluir la palabra Total."""
    grupos = [
        {'Keys': ['AWS Lambda'], 'Metrics': {'UnblendedCost': {'Amount': '2.00'}}},
    ]
    mensaje = formatear_mensaje(grupos, '2026-05-01', '2026-05-21')

    assert 'Total' in mensaje