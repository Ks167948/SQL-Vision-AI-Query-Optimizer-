# Project Title: SQL-Vision: Autonomous DB Assistant

An autonomous database performance assistant that empowers backend engineers to instantly diagnose and optimize slow SQL queries by translating complex execution plans into actionable, AI-driven insights.

## 💡 Why this works (The Breakdown):
### What it is:
An "autonomous database performance assistant" that translates "complex execution plans into actionable, AI-driven insights."
### Who it’s for:
"Backend engineers" (or software developers/DBAs).
### Why it’s useful:
It allows them to "instantly diagnose and optimize slow SQL queries" without needing to be a Postgres expert or risk breaking a production database.


## 🚀 Demo
Live Link: https://yourproject.com

## 📸 Screenshots

## ✨ Features
🤖 AI-Powered Optimization: Instantly generates "Staff Engineer" level tuning advice using local LLMs.

🛡️ Zero-Risk Sandboxing: Safely executes EXPLAIN analysis in ephemeral transactions without affecting live data.

⚡ Async Architecture: Handles heavy workloads non-blocking via a distributed Celery & Redis queue.


📊 Deep Plan Analysis: Decodes complex PostgreSQL EXPLAIN JSON output into actionable index recommendations.

🐳 Fully Containerized: Modular microservices architecture orchestrated with Docker Compose.

🔌 RESTful API: Robust backend endpoints built with Django REST Framework for easy integration.

## 🛠 Tech Stack
### Frontend:

React.js (Vite)

Tailwind CSS

Lucide React

### Backend:

Python (Django REST Framework)

Celery (Distributed Task Queue)

Redis (Message Broker)

### Database:

PostgreSQL (Primary + Sandbox Instances)

DevOps & Infrastructure:

Docker & Docker Compose

Ollama (Local LLM Inference)

## ⚙️ Installation
### Prerequisites:

Docker Desktop (Running)

Ollama (Installed & Running on host)

## 1. Clone the repo
### Bash
git clone https://github.com/Ks167948/SQL-Vision.git
cd SQL-Vision

## 2. Start the AI Model
Since the AI runs locally on your machine, you need to start the model server first:

### Bash
### Open a separate terminal
ollama run llama3

## 3. Build & Run
Launch the entire system (Frontend, Backend, Database, Redis, Worker) with one command:

### Bash
docker-compose up --build

## 4. Access the App
Frontend: http://localhost:3000

Backend API: http://localhost:8000/api/v1/analyze/

## 📂 Project Structure
```bash
sql-vision/
├── backend/                 # Django REST Framework API
│   ├── core/
│   │   ├── tasks.py         # 🧠 The "Brain": Celery Worker + AI Logic
│   │   ├── models.py        # Database Schema (Project, QueryAnalysis)
│   │   ├── views.py         # API Endpoints
│   │   └── serializers.py   # JSON Data Transformation
│   ├── config/              # Django Settings (CORS, DB Config)
│   ├── Dockerfile           # Python/Django Image Definition
│   └── requirements.txt     # Python Dependencies
│
├── frontend/                # React + Vite Application
│   ├── src/
│   │   ├── components/      # Reusable UI Components
│   │   ├── api.js           # 🔌 Axios Bridge to Backend API
│   │   ├── App.jsx          # Main Dashboard Layout
│   │   └── main.jsx         # React Entry Point
│   ├── Dockerfile           # Node.js/Vite Image Definition
│   └── tailwind.config.js   # Styling Configuration
│
├── docker-compose.yml       # 🐳 Orchestration (Web, Worker, DB, Redis)
└── README.md                # Project Documentation
```
### Problem It Solves
## 🎯 Problem Statement
Backend engineers often struggle to optimize slow SQL queries because analyzing PostgreSQL EXPLAIN plans requires deep database expertise. Furthermore, testing heavy queries on production databases is risky and can degrade live performance.

SQL-Vision solves this by providing a safe, ephemeral sandbox where queries are analyzed in isolation. It uses an AI engine to translate cryptic execution plans into clear, actionable optimization strategies—empowering developers to fix bottlenecks without needing a DBA.

## Future Improvements
### 🚀 Future Improvements
[ ] 📈 Visual Query Plan: Interactive graph visualization of the execution nodes (Scan vs. Seek).

[ ] 🤖 Multi-LLM Support: Allow users to switch between Llama3, Mistral, and GPT-4 for analysis.

[ ] 📦 Schema Import: Auto-import schema from existing live databases via connection string.

[ ] ⚡ Index Auto-Tuning: Automatically generate the exact CREATE INDEX SQL command for the user.
