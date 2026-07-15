import boto3
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()


def get_aws_client():
    """Crea el cliente de Cost Explorer. us-east-1 obligatorio.
    En Lambda usa el IAM Role automáticamente. En local usa las
    credenciales del AWS CLI o del .env."""
    return boto3.client('ce', region_name='us-east-1')

def get_parametro(nombre):
    """Lee un parámetro de AWS Systems Manager Parameter Store."""
    cliente = boto3.client('ssm', region_name='us-east-1')
    respuesta = cliente.get_parameter(
        Name=nombre,
        WithDecryption=True
    )
    return respuesta['Parameter']['Value']


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

def get_costes_diarios(cliente, dias=7):
    """Llama a Cost Explorer y devuelve el coste total de cada uno de los últimos días.

    Devuelve una lista de floats, ordenada del día más antiguo al más reciente.
    """
    hoy = datetime.today()
    inicio = (hoy - timedelta(days=dias)).strftime('%Y-%m-%d')
    fin = hoy.strftime('%Y-%m-%d')

    respuesta = cliente.get_cost_and_usage(
        TimePeriod={'Start': inicio, 'End': fin},
        Granularity='DAILY',
        Metrics=['UnblendedCost']
    )

    costes = []
    for periodo in respuesta['ResultsByTime']:
        cantidad = float(periodo['Total']['UnblendedCost']['Amount'])
        costes.append(cantidad)

    return costes


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

import statistics


def detectar_anomalia(costes_historicos, coste_ayer, umbral_sigmas=2):
    """
    Detecta si el coste de ayer es anómalo comparado con el histórico.
    
    Args:
        costes_historicos: lista de costes diarios (los días previos a ayer)
        coste_ayer: coste del día más reciente
        umbral_sigmas: cuántas desviaciones estándar considerar anómalo
    
    Returns:
        dict con: es_anomalia, media, desviacion, umbral, z_score
    """
    if len(costes_historicos) < 2:
        # No tenemos suficiente histórico para calcular σ
        return {
            'es_anomalia': False,
            'media': 0,
            'desviacion': 0,
            'umbral': 0,
            'z_score': 0,
            'motivo': 'histórico insuficiente'
        }
    
    media = statistics.mean(costes_historicos)
    desviacion = statistics.stdev(costes_historicos)
    umbral = media + (umbral_sigmas * desviacion)
    
    # Z-score, cuántas σ por encima de la media está el coste de ayer
    if desviacion > 0:
        z_score = (coste_ayer - media) / desviacion
    else:
        z_score = 0  # todos los días iguales, no hay desviación
    
    return {
        'es_anomalia': coste_ayer > umbral,
        'media': media,
        'desviacion': desviacion,
        'umbral': umbral,
        'z_score': z_score,
        'motivo': 'OK'
    }


def formatear_mensaje_anomalia(deteccion, coste_ayer):
    """Formatea el mensaje de alerta cuando se detecta una anomalía."""
    exceso = coste_ayer - deteccion['umbral']
    return (
        f"Coste de AWS más alto de lo normal\n"
        f"Ayer: ${coste_ayer:.2f}\n"
        f"Media últimos 7 días: ${deteccion['media']:.2f}\n"
        f"Ayer gastaste ${exceso:.2f} mas de lo esperado"
    )


def enviar_alerta_telegram(mensaje):
    """Envía mensaje a Telegram. Lee credenciales de Parameter Store."""
    token = get_parametro('/finops-monitor/telegram/bot-token')
    chat_id = get_parametro('/finops-monitor/telegram/chat-id')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    datos = urllib.parse.urlencode({
        'chat_id': chat_id,
        'text': mensaje
    }).encode()
    urllib.request.urlopen(url, datos)

def get_datos_demo(con_anomalia=False):
    """
    Devuelve datos simulados para pruebas locales.
    
    Args:
        con_anomalia si es true, el coste de ayer está disparado.
    
    Returns:
        (historico, coste_ayer), tupla con lista de costes históricos y coste del último día.
    """
    # Histórico realista de 7 días con poca variación
    historico = [4.20, 4.50, 4.30, 4.80, 4.40, 4.60, 4.50]
    
    if con_anomalia:
        coste_ayer = 12.30   # claramente fuera del rango normal
    else:
        coste_ayer = 4.55    # dentro del rango normal
    
    return historico, coste_ayer

def handler(event, context):
    """Función principal del handler. Soporta modo --demo desde CLI."""
    try:
        # Detectar si estamos en modo demo
        modo_demo = '--demo' in sys.argv
        con_anomalia = '--anomalia' in sys.argv
        
        if modo_demo:
            # MODO DEMO datos simulados
            historico, coste_ayer = get_datos_demo(con_anomalia=con_anomalia)
            deteccion = detectar_anomalia(historico, coste_ayer)
            
            if deteccion['es_anomalia']:
                mensaje = formatear_mensaje_anomalia(deteccion, coste_ayer)
            else:
                mensaje = (
                    f"✅ [DEMO] Coste de ayer dentro del rango normal\n\n"
                    f"Coste de ayer: ${coste_ayer:.4f}\n"
                    f"Media últimos 7 días: ${deteccion['media']:.4f}\n"
                    f"Umbral de alerta: ${deteccion['umbral']:.4f}"
                )
        else:
            # MODO REAL datos de AWS
            cliente = get_aws_client()
            inicio, fin = get_date_range()
            grupos = get_costes(cliente, inicio, fin)
            mensaje = formatear_mensaje(grupos, inicio, fin)
        
        enviar_alerta_telegram(mensaje)
        return {'statusCode': 200, 'body': 'OK'}
    
    except Exception as e:
        error = f"AWS FinOps Monitor — Error: {str(e)}"
        enviar_alerta_telegram(error)
        return {'statusCode': 500, 'body': error}


if __name__ == "__main__":
    handler(None, None)