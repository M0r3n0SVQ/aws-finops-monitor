# AWS FinOps Monitor

Monitor de costes de AWS con alertas a Telegram.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazon-aws)
![Terraform](https://img.shields.io/badge/IaC-Terraform-purple?logo=terraform)

## Qué hace

Cada 24h se conecta a Cost Explorer, lee los costes del mes, los agrupa por servicio y manda el resumen a Telegram. También compara el coste del día con los 7 anteriores para detectar gastos anómalos.

## Stack

Python + boto3, desplegado en Lambda con EventBridge para que se ejecute solo. Todo gestionado con Terraform y desplegado vía GitHub Actions.

## Estructura

```
aws-finops-monitor/
├── .github/workflows/deploy.yml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── monitor.py
├── requirements.txt
└── .env.example
```

## Probarlo en local

Como mi cuenta de AWS está prácticamente a 0€, hay un modo demo con datos simulados:

```bash
python monitor.py --demo            # caso normal
python monitor.py --demo --anomalia # caso alerta
```

En Lambda los flags se ignoran, usa datos reales.

## Setup

```bash
git clone https://github.com/M0r3n0SVQ/aws-finops-monitor.git
cd aws-finops-monitor
python -m venv venv
source venv/bin/activate    # o venv\Scripts\activate en Windows
pip install -r requirements.txt
cp .env.example .env        # rellenar las 4 variables
python monitor.py
```

## Despliegue

```bash
cd terraform
terraform init
terraform apply
```

## Estado

Hecho:
- Lectura de costes desde Cost Explorer + alertas Telegram
- Despliegue en Lambda con EventBridge diario
- Terraform + GitHub Actions
- Detección de anomalías con media y desviación
- Modo demo para iterar en local

Pendiente:
- Tests con pytest
- Detección de anomalías con datos reales de Cost Explorer (ahora solo funciona en modo demo)
