#  CropGuard Ghana

> *AI-powered crop disease detection chatbot for Ghanaian farmers*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-green.svg)](https://flask.palletsprojects.com/)

---

##  Live Application
**URL:** http://20.160.5.97:5000

---

##  Architecture
```
                    ┌─────────────────────────────────────┐
                    │         GitHub Actions CI/CD         │
                    │  CI: lint → test → trivy → tfsec    │
                    │  CD: build → push ACR → ansible      │
                    └────────────────┬────────────────────┘
                                     │
                    ┌────────────────▼────────────────────┐
                    │      Azure Container Registry        │
                    │       cropguardacr.azurecr.io        │
                    └────────────────┬────────────────────┘
                                     │
┌─────────────────── Azure VNet (10.0.0.0/16) ───────────────────────────┐
│                                                                          │
│  Public Subnet (10.0.1.0/24)      Private Subnet (10.0.2.0/24)         │
│  ┌─────────────────────┐          ┌──────────────────────┐             │
│  │   Bastion Host      │─── SSH ──▶   App VM             │             │
│  │   52.157.194.161    │          │   Docker + Flask      │             │
│  └─────────────────────┘          │   :5000               │             │
│                                   └──────────────────────┘             │
│  ┌─────────────────────────────────────────────────────┐               │
│  │         Azure MySQL Flexible Server                  │               │
│  │         cropguard-mysql.mysql.database.azure.com     │               │
│  └─────────────────────────────────────────────────────┘               │
└──────────────────────────────────────────────────────────────────────────┘
```

---

##  Problem Statement

Ghana loses an estimated **30–40% of crop yields** annually to diseases and pests, yet most smallholder farmers lack timely access to expert agronomic advice. An extension officer in Ghana serves an average of **1,500+ farmers** — making personal farm visits nearly impossible. CropGuard closes this gap by putting a 24/7 crop disease expert in every farmer's pocket, accessible via any web-enabled device or smartphone.

---

##  Target Users

- **Smallholder farmers** across Ghana's agricultural belts (Brong-Ahafo, Volta, Northern Region)
- **Agricultural extension officers** at Ministry of Food & Agriculture (MOFA)
- **Cooperative societies & farmer groups** managing collective farms
- **Agritech NGOs** deploying field support tools

---

##  Core Features

| # | Feature | Status |
|---|---------|--------|
| 1 | **Conversational Disease Detection** — Describe symptoms in plain English |  MVP |
| 2 | **Treatment & Prevention Advice** — Actionable steps for each disease |  MVP |
| 3 | **Crop-Level Disease Browser** — Ask about all diseases for a specific crop |  MVP |
| 4 | **Multi-language Support (Twi/Dagbani)** — Local language greetings |  In Progress |
| 5 | **SMS/USSD Integration** — Access via basic feature phones |  Backlog |

---

##  Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11, Flask 3.x |
| **AI/NLP** | Rule-based NLP engine (keyword + alias matching) |
| **Frontend** | HTML5, Vanilla JS, Custom CSS |
| **Database** | Azure MySQL Flexible Server |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Infrastructure** | Terraform (Azure VNet, VM, Bastion, MySQL, ACR) |
| **Configuration** | Ansible |
| **Security Scanning** | Trivy (container), tfsec (IaC) |
| **Testing** | pytest, pytest-flask |

---

##  Getting Started

### Prerequisites
- Python 3.11+
- pip
- Git
- Docker & Docker Compose
- Terraform
- Ansible

### Run Locally
```bash
git clone https://github.com/maabu025/wheather_checker.git
cd wheather_checker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/app.py
# Open http://localhost:5000
```

### Run with Docker
```bash
docker-compose up --build
# Open http://localhost:5000
```

### Run Tests
```bash
PYTHONPATH=src pytest test_chatbot.py -v
```

### Infrastructure Setup (Terraform)
```bash
cd terraform
terraform init
terraform apply
```

### Configuration Management (Ansible)
```bash
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
```

---

##  Project Structure
```
wheather_checker/
├── src/
│   ├── app.py
│   └── templates/
│       └── index.html
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
├── ansible/
│   ├── playbook.yml
│   └── inventory.ini
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── test_chatbot.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

##  REST API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Send a message to the chatbot |
| `GET` | `/api/diseases` | List all diseases |
| `GET` | `/api/diseases/<name>` | Get details on a specific disease |
| `GET` | `/health` | Service health check |

---

##  Supported Crops & Diseases

| Crop | Diseases |
|------|----------|
|  Maize | Maize Streak Virus, Northern Corn Leaf Blight, Fall Armyworm |
|  Cocoa | Black Pod Disease, Cocoa Swollen Shoot Virus |
|  Cassava | Cassava Mosaic Disease, Cassava Bacterial Blight |
|  Tomato | Tomato Late Blight, Tomato Leaf Curl |
|  Yam | Yam Anthracnose |

---

##  Team Members

| Name | Role | GitHub |
|------|------|--------|
| Mariam Abu | Team Lead / Backend Developer / QA | maabu025 |
| Alberta Logozaga | Frontend Developer / DevOps Engineer | Albert499 |

---

##  Disclaimer

CropGuard provides guidance based on a curated knowledge base. For critical crop health decisions, always consult a certified agronomist or your local **MOFA** extension officer.

---

##  License

MIT License — see [LICENSE](LICENSE) for details.
