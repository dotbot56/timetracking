# Timetracking

This repository contains a minimal scaffold for a time tracking application for a construction company.

## Structure

- `backend/` – lightweight Python backend with in-memory storage and tests.
- `frontend/` – Next.js frontend that fetches time entries from the backend.

## Backend

The backend uses only the Python standard library.

```bash
pytest backend
python -m backend.server
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend to run on `http://localhost:8000`.