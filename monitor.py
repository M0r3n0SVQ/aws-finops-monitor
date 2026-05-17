import boto3
import os
import urllib.request
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def get_aws_client():
    """Crea el cliente de Cost Explorer. us-east-1 obligatorio."""
    return boto3.client(
        'ce',
        region_name='us-east-1',
        aws_access_key_id=os.getenv('FINOPS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('FINOPS_SECRET_KEY')
    )


def get_date_range():
    """Devuelve (inicio_mes, hoy) en formato YYYY-MM-DD."""
    hoy = datetime.today()
    inicio_mes = hoy.replace(day=1).strftime('%Y-%m-%d')
    hoy_str = hoy.strftime('%Y-%m-%d')
    return inicio_mes, hoy_str


def get_costes(cliente, inicio, fin):
    """Llama a AWS Cost Explorer para obtener costes por servicio."""
    respuesta = cliente.get_cost_and_usage(
        TimePeriod={'Start': inicio, 'End': fin},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )
    return respuesta['ResultsByTime'][0]['Groups']


def formatear_mensaje(grupos, inicio, fin):
    """Formatea el mensaje."""
    mensaje = f"Costes AWS — {inicio} al {fin}\n\n"
    total = 0

    for servicio in grupos:
        nombre = servicio['Keys'][0]
        coste = float(servicio['Metrics']['UnblendedCost']['Amount'])
        if coste > 0:
            mensaje += f"{nombre}: ${coste:.4f}\n"
            total += coste

    mensaje += f"\n Total: ${total:.4f}"
    return mensaje


def enviar_alerta_telegram(mensaje):
    """Envía mensaje a Telegram."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    datos = urllib.parse.urlencode({
        'chat_id': chat_id,
        'text': mensaje
    }).encode()
    urllib.request.urlopen(url, datos)


def handler(event, context):
    """Función principal del handler."""
    try:
        cliente = get_aws_client()
        inicio, fin = get_date_range()
        grupos = get_costes(cliente, inicio, fin)
        mensaje = formatear_mensaje(grupos, inicio, fin)
        print(mensaje)
        enviar_alerta_telegram(mensaje)
        return {'statusCode': 200, 'body': 'OK'}
    except Exception as e:
        error = f"AWS FinOps Monitor — Error: {str(e)}"
        print(error)
        enviar_alerta_telegram(error)
        return {'statusCode': 500, 'body': error}


if __name__ == "__main__":
    handler(None, None)