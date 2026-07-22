from unittest.mock import patch, MagicMock
from monitor import handler


@patch('monitor.enviar_alerta_telegram')
@patch('monitor.get_costes_diarios')
@patch('monitor.get_costes')
@patch('monitor.get_aws_client')
def test_handler_manda_alerta_si_hay_anomalia(
    mock_get_aws_client, mock_get_costes, mock_get_costes_diarios, mock_enviar_alerta
):
    """Si el coste de ayer es anómalo, debe mandarse un segundo mensaje de alerta."""
    mock_get_aws_client.return_value = MagicMock()
    mock_get_costes.return_value = []
    # 6 días normales + 1 día disparado
    mock_get_costes_diarios.return_value = [4.20, 4.50, 4.30, 4.80, 4.40, 4.60, 20.00]

    handler(None, None)

    # Se debe haber llamado dos veces, resumen mensual y alerta de anomalía
    assert mock_enviar_alerta.call_count == 2


@patch('monitor.enviar_alerta_telegram')
@patch('monitor.get_costes_diarios')
@patch('monitor.get_costes')
@patch('monitor.get_aws_client')
def test_handler_no_manda_alerta_si_no_hay_anomalia(
    mock_get_aws_client, mock_get_costes, mock_get_costes_diarios, mock_enviar_alerta
):
    """Si el coste de ayer es normal, solo debe mandarse el resumen mensual."""
    mock_get_aws_client.return_value = MagicMock()
    mock_get_costes.return_value = []
    # 7 días con poca variación, ninguno anómalo
    mock_get_costes_diarios.return_value = [4.20, 4.50, 4.30, 4.80, 4.40, 4.60, 4.55]

    handler(None, None)

    # Solo se debe haber llamado una vez, el resumen mensual
    assert mock_enviar_alerta.call_count == 1