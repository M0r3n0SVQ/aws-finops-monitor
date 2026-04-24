# 🔍 AWS FinOps Monitor

> Monitor de costes de AWS con alertas automáticas a Telegram

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazon-aws)
![Terraform](https://img.shields.io/badge/IaC-Terraform-purple?logo=terraform)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-green)

Proyecto práctico construido durante el Programa Avanzado en Cloud Computing de UNIR.

---

## ¿Qué hace?

Cada 24 horas, automáticamente:

1. Se conecta a AWS Cost Explorer y lee los costes del mes
2. Agrupa los gastos por servicio
3. Manda un resumen a Telegram
4. Si hay algún error, también lo notifica

---

## 🏗️ Arquitectura

```
EventBridge (cada 24h)
        ↓
   AWS Lambda
        ↓
AWS Cost Explorer API
        ↓
  Bot de Telegram
        ↓
     📱 Móvil
```

Toda la infraestructura desplegada con Terraform.

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|-----------|-----|
| Python 3.14 | Script principal |
| boto3 | SDK oficial de AWS |
| AWS Lambda | Ejecución serverless |
| AWS EventBridge | Automatización diaria |
| AWS Cost Explorer | Lectura de costes |
| Terraform | Infraestructura como código |
| Telegram Bot API | Alertas al móvil |

---

## 🚀 Instalación en local

**1. Clona el repositorio**

```bash
git clone https://github.com/M0r3n0SVQ/aws-finops-monitor.git
cd aws-finops-monitor
```

**2. Crea el entorno virtual**

```bash
python -m venv venv
venv\Scripts\activate
pip install boto3 python-dotenv requests
```

**3. Crea el archivo `.env`**

```
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_DEFAULT_REGION=eu-south-2
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id
```

**4. Ejecuta**

```bash
python monitor.py
```

---

## ☁️ Despliegue con Terraform

```bash
cd terraform
terraform init
terraform apply
```

---

## ✅ Estado del proyecto

✅ Script Python conectado a AWS Cost Explorer  
✅ Alertas automáticas a Telegram  
✅ Desplegado en AWS Lambda  
✅ Automatización diaria con EventBridge  
✅ Infraestructura como código con Terraform  

**Próximos pasos:**  
Detección de anomalías  
Pipeline CI/CD