import boto3
import os
import sys
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
        f"🚨 ALERTA: Coste anómalo detectado\n\n"
        f"Coste de ayer: ${coste_ayer:.4f}\n"
        f"Media últimos 7 días: ${deteccion['media']:.4f}\n"
        f"Umbral de alerta: ${deteccion['umbral']:.4f}\n\n"
        f"El coste de ayer supera el umbral en ${exceso:.4f}"
    )


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