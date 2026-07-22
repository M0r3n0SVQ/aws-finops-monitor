# AWS FinOps Monitor

Monitor de costes de AWS con alertas a Telegram.

[![Tests](https://github.com/M0r3n0SVQ/aws-finops-monitor/actions/workflows/deploy.yml/badge.svg)](https://github.com/M0r3n0SVQ/aws-finops-monitor/actions)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazon-aws)
![Terraform](https://img.shields.io/badge/IaC-Terraform-purple?logo=terraform)
![License](https://img.shields.io/badge/license-MIT-green)

## Qué hace

- Lee los costes de AWS Cost Explorer agrupados por servicio
- Compara el coste de ayer con el histórico de los últimos días y avisa si se sale de lo normal, indicando cuánto por encima está
- Manda el resumen diario a Telegram, y también una alerta si algo falla en la ejecución
- Incluye un modo demo (`--demo`) para probar la lógica sin necesidad de credenciales reales de AWS

## Arquitectura

EventBridge Scheduler dispara la Lambda una vez al día → la Lambda lee Cost Explorer con boto3 → calcula si hay anomalía → manda el mensaje a Telegram.

La autenticación con AWS se hace con el rol IAM de la propia Lambda, sin claves de acceso estáticas. Las credenciales de Telegram se guardan cifradas en Parameter Store, no en variables de entorno.

Desplegado en `eu-south-2` (España). Cost Explorer solo tiene endpoint en `us-east-1`, así que la Lambda usa esa región para las llamadas a `ce:GetCostAndUsage` aunque el resto de recursos vivan en `eu-south-2`.

## Tecnologías

- Python 3.13
- boto3 (Cost Explorer, IAM, Parameter Store)
- Telegram Bot API
- Terraform — infraestructura como código: rol IAM, función Lambda, EventBridge Scheduler
- pytest — tests de la detección de anomalías, las llamadas a Cost Explorer y el formateo de mensajes
- GitHub Actions — CI/CD: tests automáticos en cada push y despliegue a Lambda si pasan

## Probarlo en local

```bash
git clone https://github.com/M0r3n0SVQ/aws-finops-monitor.git
cd aws-finops-monitor
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env  # Rellena tus credenciales de AWS y Telegram
python monitor.py --demo
```

El modo `--demo` simula los datos para no tener que tocar AWS de verdad. Para forzar una anomalía de prueba: `python monitor.py --demo --anomalia`.

## Tests

```bash
pytest -v
```

## Estado del proyecto

Desplegado y corriendo en producción, con despliegue automático desde GitHub Actions en cada push a master.

## Licencia

MIT — ver [LICENSE](LICENSE).
