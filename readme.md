# AWS FinOps Monitor

Monitor de costes de AWS que manda alertas automáticas a Telegram cuando detecta gastos.

Construido durante el programa avanzado en Cloud Computing de UNIR como proyecto práctico.

## Qué hace

- Se conecta a AWS Cost Explorer y lee los costes del mes actual
- Agrupa los costes por servicio
- Manda un resumen automático a Telegram
- Notifica también si hay algún error, para saber siempre que el sistema está funcionando

## Arquitectura

AWS Cost Explorer API → Python (boto3) → Telegram Bot API → Móvil

## Tecnologías

- Python 3.14
- boto3 - SDK oficial de AWS
- Telegram Bot API
- AWS Cost Explorer
- AWS IAM

## Instalación

1. Clona el repositorio

git clone https://github.com/M0r3n0SVQ/aws-finops-monitor.git

2. Crea el entorno virtual e instala dependencias

python -m venv venv
venv\Scripts\activate
pip install boto3 python-dotenv requests

3. Crea un archivo .env con tus credenciales

AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_DEFAULT_REGION=eu-south-2
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id

4. Ejecuta el script

python monitor.py

## Estado del proyecto

En desarrollo — próximos pasos:
- Automatización con AWS Lambda
- Detección de anomalías
- Infraestructura como código con Terraform