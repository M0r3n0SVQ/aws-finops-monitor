"""Tests para la lógica de detección de anomalías."""
from monitor import detectar_anomalia


def test_detecta_anomalia_con_coste_disparado():
    """Un coste muy por encima del histórico debe marcarse como anomalía."""
    historico = [4.0, 4.0, 4.0, 4.0, 4.0]
    coste_ayer = 100.0

    resultado = detectar_anomalia(historico, coste_ayer)

    assert resultado['es_anomalia'] is True


def test_no_detecta_anomalia_con_coste_normal():
    """Un coste dentro del rango normal NO debe marcarse como anomalía."""
    historico = [4.0, 4.5, 4.2, 4.3, 4.4]
    coste_ayer = 4.35

    resultado = detectar_anomalia(historico, coste_ayer)

    assert resultado['es_anomalia'] is False


def test_calcula_media_correctamente():
    """La media de [2, 4, 6] debe ser 4."""
    historico = [2.0, 4.0, 6.0]
    coste_ayer = 4.0

    resultado = detectar_anomalia(historico, coste_ayer)

    assert resultado['media'] == 4.0

def test_historico_insuficiente_no_es_anomalia():
    """Con menos de 2 datos no se puede calcular: no debe petar ni marcar anomalía."""
    historico = [4.0]
    coste_ayer = 100.0

    resultado = detectar_anomalia(historico, coste_ayer)

    assert resultado['es_anomalia'] is False