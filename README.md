# Airline Resolution Agent

Live Demo: https://airline-resolution-agent-njutqh867-sakshampachauri558-2538.vercel.app/

A simple airline customer support app that helps resolve booking and flight-related issues using a backend workflow and a frontend dashboard.

## Features
- Customer and booking lookup
- Support request handling
- Policy-based recommendations
- Action suggestions and escalation flow
- Modern dashboard UI

## Tech Stack
- Next.js
- FastAPI
- Python
- LangGraph
- Tailwind CSS

## Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
