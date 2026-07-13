# 🚀 AI Lead Intelligence System

An AI-powered B2B lead generation and research platform that discovers companies, enriches business data, detects buying signals, and prioritizes high-value prospects using automated workflows and intelligent scoring.


![Landing Page](Screenshots/landing-page.png)


## 📌 Overview

The **AI Lead Intelligence System** helps sales teams, marketing agencies, and businesses find potential customers faster by automating the lead research process.

Instead of manually searching hundreds of companies, this platform:

* Collects company information
* Enriches lead data
* Detects business signals
* Scores prospects based on buying potential
* Displays prioritized leads in an interactive dashboard

The goal is to reduce manual prospecting time and help teams focus on the most valuable opportunities.

---

## 🚀 Live Demo

🌐 Live Application:
https://ai-lead-intelligence-system-1.onrender.com

🎥 Loom Walkthrough:
https://www.loom.com/share/9425cb2bde244809b1dca95775a2838b

📂 Source Code:
https://github.com/sam-uelt50/ai-lead-intelligence-system
# ✨ Key Features

## 🔍 Automated Company Discovery

* Collect company information from multiple sources
* Extract business details automatically
* Store and organize company profiles

## 🤖 AI Lead Scoring

The system evaluates leads using intelligent scoring factors:

* Company size
* Industry relevance
* Technology usage
* Growth signals
* Business activity

Each lead receives a priority score to identify the best opportunities.

## 📊 Lead Intelligence Dashboard

Features include:

* Lead overview
* Company information
* Priority ranking
* Signal detection
* Research results
* Lead filtering

## 📈 Buying Signal Detection

Detects indicators that a company may need services:

Examples:

* New technology adoption
* Company growth
* Hiring activity
* Website changes
* Digital transformation signals

## 🌐 Data Enrichment

Enhances company profiles with:

* Industry information
* Website data
* Technology stack
* Company details

## ⚡ API-Based Architecture

Built with a scalable backend architecture:

* REST API endpoints
* Modular services
* Database integration
* Frontend-backend communication

---
## 📸 Screenshots

### Landing Page

![Landing Page](Screenshots/landing-page.png)


### AI Lead Dashboard

![AI Lead Dashboard](Screenshots/dashbroad.png)


### Company Leads Analysis

![Company Leads](Screenshots/companies-leads.png)


### Company Details

![Company Details](Screenshots/companies-details.png)


### Decision Makers

![Decision Makers](Screenshots/decison-makers.png)
# 🏗️ System Architecture

```
                    User
                     |
                     |
              Frontend Dashboard
              (HTML/CSS/JS)
                     |
                     |
                FastAPI Backend
                     |
      --------------------------------
      |              |               |
 Lead Service   Research Service   Signal Detection
      |              |               |
      --------------------------------
                     |
              Database Storage
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* REST API
* Pydantic
* MongoDB
* SQL/SQLite support

## Frontend

* HTML5
* CSS3
* JavaScript

## AI & Automation

* AI-powered lead scoring
* Automated research workflows
* Data enrichment pipelines
* Signal analysis

## Development Tools

* Git
* GitHub
* VS Code
* Virtual Environment

---

# 📂 Project Structure

```
AI-Lead-Intelligence-System/

│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   └── api/
│   │
│   ├── services/
│   │   ├── lead_enricher.py
│   │   ├── scoring_services.py
│   │   ├── research_service.py
│   │   └── signal_detector.py
│   │
│   ├── models/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── screenshots/
│
├── README.md
└── .gitignore
```

---

# ⚙️ Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/sam-uelt50/ai-lead-intelligence-system.git

cd ai-lead-intelligence-system
```

---

# Backend Setup

## 2. Create Virtual Environment

Windows:

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
cd backend

pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create:

```
backend/.env
```

Add your own API keys:

```
OPENAI_API_KEY=your_key_here

DATABASE_URL=your_database_url

MONGODB_URI=your_mongodb_url
```

---

# Run Backend

Inside backend folder:

```bash
uvicorn main:app --reload
```

Backend will run:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

---

# Frontend Setup

Open:

```
frontend/index.html
```

or run with a local server.

Example:

```bash
python -m http.server 5500
```

Open:

```
http://localhost:5500
```

---

# 📊 Example Workflow

```
Company Discovery
        ↓
Data Collection
        ↓
Information Enrichment
        ↓
AI Analysis
        ↓
Lead Scoring
        ↓
Priority Dashboard
        ↓
Sales Outreach
```

---

# 🎯 Use Cases

## Marketing Agencies

Find companies that need:

* Website development
* Automation services
* AI solutions
* Digital marketing

## Sales Teams

Identify:

* High-value prospects
* Growing companies
* Active buyers

## Freelancers

Generate targeted leads instead of random outreach.

---

# 🚀 Future Improvements

Planned features:

* [ ] Real-time web scraping pipeline
* [ ] LinkedIn integration
* [ ] Email outreach automation
* [ ] CRM integration
* [ ] AI-generated personalized messages
* [ ] Cloud deployment
* [ ] User authentication
* [ ] Advanced machine learning ranking model

---


**Samuel Tesema**

Electrical & Computer Engineer
AI Automation Developer

GitHub:

https://github.com/sam-uelt50

---

# ⭐ Why This Project Matters

This project demonstrates practical skills in:

* AI application development
* Backend engineering
* Data processing
* Automation systems
* Business intelligence dashboards
* Building tools for real-world sales problems

It represents a complete AI-powered SaaS-style application from data collection to user interface.
