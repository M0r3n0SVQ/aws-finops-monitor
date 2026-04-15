import boto3
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests

load_dotenv()
def enviar_alerta_telegram(mensaje):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': mensaje
    }
    requests.get(url, params=params)

def get_costes_mes_actual():
    try:
        cliente = boto3.client(
            'ce',
            region_name='us-east-1',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

        hoy = datetime.today()
        inicio_mes = hoy.replace(day=1).strftime('%Y-%m-%d')
        hoy_str = hoy.strftime('%Y-%m-%d')

        respuesta = cliente.get_cost_and_usage(
            TimePeriod={
                'Start': inicio_mes,
                'End': hoy_str
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
        )

        total = 0
        mensaje = f"Costes AWS — {inicio_mes} al {hoy_str}\n\n"

        for servicio in respuesta['ResultsByTime'][0]['Groups']:
            nombre = servicio['Keys'][0]
            coste = float(servicio['Metrics']['UnblendedCost']['Amount'])
            if coste > 0:
                mensaje += f"{nombre}: ${coste:.4f}\n"
                total += coste

        mensaje += f"\n Total: ${total:.4f}"
        print(mensaje)
        enviar_alerta_telegram(mensaje)

    except Exception as e:
        error = f"AWS FinOps Monitor — Error: {str(e)}"
        print(error)
        enviar_alerta_telegram(error)

if __name__ == "__main__":
    get_costes_mes_actual()