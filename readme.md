# 🔍 AWS FinOps Monitor

> Monitor de costes de AWS con alertas automáticas a Telegram

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazon-aws)
![Terraform](https://img.shields.io/badge/IaC-Terraform-purple?logo=terraform)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-green)
![Last Commit](https://img.shields.io/github/last-commit/M0r3n0SVQ/aws-finops-monitor)

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
git push
    ↓
GitHub Actions (CI/CD)
    ↓
AWS Lambda
    ↓
EventBridge (cada 24h)
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
| GitHub Actions | Pipeline CI/CD |
| Telegram Bot API | Alertas al móvil |

---

## 📁 Estructura

```
aws-finops-monitor/
├── .github/workflows/deploy.yml    # Pipeline CI/CD
├── terraform/                       # Infraestructura como código
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── monitor.py                       # Lógica principal
├── requirements.txt                 # Dependencias Python
├── .env.example                     # Plantilla de variables
└── README.md
```

---

## 🚀 Instalación en local

**1. Clona el repositorio**

```bash
git clone https://github.com/M0r3n0SVQ/aws-finops-monitor.git
cd aws-finops-monitor
```

**2. Crea el entorno virtual**

```bash
python3 -m venv venv

# Linux / macOS
source venv/bin/activate

# Linux con Fish shell
source venv/bin/activate.fish

# Windows
venv\Scripts\activate
```

**3. Instala las dependencias**

```bash
pip install -r requirements.txt
```

**4. Crea el archivo `.env`** a partir de `.env.example`:

```
FINOPS_ACCESS_KEY=tu_access_key
FINOPS_SECRET_KEY=tu_secret_key
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id
```

**5. Ejecuta**

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
✅ Pipeline CI/CD con GitHub Actions  

**Próximos pasos:**  
🔜 Detección de anomalías en costes  
🔜 Tests automáticos en el pipeline  
