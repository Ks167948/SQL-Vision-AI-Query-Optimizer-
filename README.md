SQL Vision AI (WIP)
SQL Vision is an autonomous database performance assistant. It safely executes SQL queries in a sandboxed transaction, extracts the Postgres execution plan (EXPLAIN JSON), and uses a local Large Language Model (LLM) to provide "Staff Engineer" level optimization advice.

Current Status: Backend & AI Pipeline are 100% Operational. Frontend is currently under construction.

🚀 Tech Stack
Core: Python, Django REST Framework

Database: PostgreSQL (Primary + Sandbox Instances)

Async Processing: Celery + Redis

AI/LLM: Ollama (Llama3 / Mistral) running locally

Infrastructure: Docker Compose

Frontend: React + Vite + Tailwind CSS (In Progress)

🛠️ Prerequisites
Docker Desktop installed and running.

Ollama installed on your host machine.

Run a model: ollama run llama3 (or mistral)

Note: The system connects to Ollama via host.docker.internal.

⚡ Quick Start
1. Clone & Setup
Bash
git clone https://github.com/Ks167948/SQL-Vision.git
cd SQL-Vision
2. Run the System
Bash
docker-compose up --build
Wait until you see the Celery worker log: celery@... ready.

3. Usage (Via API)
Since the Frontend is WIP, use the browsable API to test the system.

Step A: Create a Project (Define your Schema)

Go to: http://127.0.0.1:8000/api/v1/projects/

Fill out the form:

Name: Test DB

Database Type: PostgreSQL

Schema DDL:

SQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
Click POST. Copy the id from the response.

Step B: Analyze a Query

Go to: http://127.0.0.1:8000/api/v1/analyze/

Click "Raw Data" and use this JSON:

JSON
{
  "project": "PASTE_YOUR_PROJECT_ID_HERE",
  "raw_sql": "SELECT * FROM users WHERE email = 'test@example.com'"
}
Click POST.

Initial Status: PENDING

Step C: Get Results

Click the "GET" button (top right) to refresh the list.

Scroll to the bottom.

Status: COMPLETED

AI Suggestion: You should see advice (e.g., "Add an index on the email column...").

📂 Project Architecture
sql-vision/
├── backend/            # Django API & Celery Tasks
│   ├── core/tasks.py   # The "Brain": Sandbox Logic + AI connection
├── frontend/           # React App (WIP)
├── docker-compose.yml  # Orchestration
🚧 Roadmap
[x] Backend API: Project & Analysis endpoints.

[x] Sandboxing: Safe transaction rollback for EXPLAIN.

[x] AI Integration: Connection to local Ollama instance.

[ ] Frontend: React Dashboard for visualization. (Next Step)

[ ] Visualizer: Graphical view of Postgres Query Plans.

Created by Kishore
