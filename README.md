# Timetracking

This repository contains a minimal scaffold for a time tracking application for a construction company.

## Structure

- `backend/` – FastAPI service with in-memory storage and tests.
- `frontend/` – Next.js frontend that fetches time entries from the backend.

## Backend

```bash
pip install -r backend/requirements.txt
pytest backend
uvicorn backend.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend to run on `http://localhost:8000`.
