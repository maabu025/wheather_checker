#  CropGuard Ghana

> *AI-powered crop disease detection chatbot for Ghanaian farmers*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-green.svg)](https://flask.palletsprojects.com/)

---

##  Problem Statement

Ghana loses an estimated **30–40% of crop yields** annually to diseases and pests, yet most smallholder farmers lack timely access to expert agronomic advice. An extension officer in Ghana serves an average of **1,500+ farmers** — making personal farm visits nearly impossible. CropGuard closes this gap by putting a 24/7 crop disease expert in every farmer's pocket, accessible via any web-enabled device or smartphone.

Farmers can describe what they observe — yellowing leaves, spots, pest damage — and CropGuard identifies the likely disease, explains the cause, and gives step-by-step treatment and prevention advice, all tailored to Ghana's major crops.

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
| 1 | **Conversational Disease Detection** — Describe symptoms in plain English; chatbot identifies likely disease from a knowledge base of 10+ Ghanaian crop diseases |  MVP |
| 2 | **Treatment & Prevention Advice** — Detailed, actionable treatment steps and prevention strategies for each identified disease |  MVP |
| 3 | **Crop-Level Disease Browser** — Ask about all diseases affecting a specific crop (maize, cocoa, cassava, tomato, yam) |  MVP |
| 4 | **Multi-language Support (Twi/Dagbani)** — Respond to local greetings; future: full local language support |  In Progress |
| 5 | **SMS/USSD Integration** — Allow farmers without smartphones to access CropGuard via basic feature phones |  Backlog |

---

##  Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11, Flask 3.x |
| **AI/NLP** | Rule-based NLP engine (keyword + alias matching); upgradeable to Claude/GPT |
| **Frontend** | HTML5, Vanilla JS, Custom CSS |
| **Database** | In-memory KB (dev) → PostgreSQL + vector search (prod) |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Infrastructure** | Terraform (AWS ECS / Render) |
| **Testing** | pytest, pytest-flask |

---

##  Getting Started

### Prerequisites

- Python 3.11 or higher
- pip
- Git

### Installation & Running Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_ORG/cropguard-ghana.git
cd cropguard-ghana

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env if needed (defaults work for local development)

# 5. Run the app
python src/app.py

# 6. Open your browser at:
#    http://localhost:5000
```

### Running with Docker

```bash
docker-compose up --build
# App available at http://localhost:5000
```

### Running Tests

```bash
pytest tests/ -v
```

---

##  Chatbot Usage Examples

Once running, try these in the chatbot:

| You type | CropGuard responds |
|----------|--------------------|
| `hello` | Welcome message with suggestions |
| `My maize has yellow streaks` | Identifies Maize Streak Virus |
| `Tell me about fall armyworm` | Full disease info + treatment |
| `What diseases affect cocoa?` | Lists all cocoa diseases |
| `black pod disease` | Black pod details + copper fungicide advice |
| `list crops` | All 10 supported diseases across 5 crops |
| `help` | Usage guide |

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

##  Project Structure

```
cropguard-ghana/
├── src/
│   ├── app.py                  # Flask app + chatbot engine + REST API
│   └── templates/
│       └── index.html          # Chat interface
├── tests/
│   └── test_chatbot.py         # 25+ pytest tests
├── .github/
│   ├── CODEOWNERS
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

##  REST API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Send a message to the chatbot |
| `GET` | `/api/diseases` | List all diseases (optional: `?crop=maize`) |
| `GET` | `/api/diseases/<name>` | Get full details on a specific disease |
| `GET` | `/health` | Service health check |

**Example chat request:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "My maize leaves have yellow streaks"}'
```

---

##  Team Members

| Name | Role | GitHub |
|------|------|--------|
| Mariam Abu | Team Lead / Backend Developer/QA / Knowledge Base | maabu025 |
| Alberta Logozaga | Frontend Developer/DevOps Engineer | Albert499 |

---

##  Disclaimer

CropGuard provides guidance based on a curated knowledge base. For critical crop health decisions, always consult a certified agronomist or your local **Ministry of Food and Agriculture (MOFA)** extension officer.

---

##  License

MIT License — see [LICENSE](LICENSE) for details.

##  Running with Docker Compose

### Prerequisites
- [Docker](https://www.docker.com/get-started) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### Start the app
```bash
# Build and start all services
docker-compose up --build

# App available at:
http://localhost:5000
```

### Run in background (detached mode)
```bash
docker-compose up -d --build
```

### Stop the app
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f web
```

### Environment Variables
Copy `.env.example` to `.env` before running:
```bash
cp .env.example .env
```
# test
