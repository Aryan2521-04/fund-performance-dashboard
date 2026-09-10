# Fund Performance Dashboard

A full-stack app for tracking private equity / VC fund cash flows and computing standard performance metrics — IRR, TVPI, and DPI — from contribution, distribution, and NAV data.

**Status:** early development. Backend scaffold and metrics engine (IRR/TVPI/DPI) in progress; API routes and frontend UI not yet built.

## Why

Fund performance is usually reported through opaque spreadsheets. This project models the underlying cash-flow math directly — including a hand-rolled XIRR solver (Newton/Brent's method over irregular real dates, not just evenly-spaced periods) — and exposes it through a simple API and dashboard.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Pydantic, pytest
- **Frontend:** React + Vite
- **Infra:** Docker, GitHub Actions (CI)

## Metrics

- **IRR** — annualized internal rate of return, computed from actual cash flow dates (not assumed regular periods)
- **TVPI** — Total Value to Paid-In: `(distributions + NAV) / contributions`
- **DPI** — Distributions to Paid-In: `distributions / contributions`

## Project Structure

```
backend/    FastAPI app: models, schemas, CRUD, metrics engine, API routes
frontend/   React + Vite dashboard
```

## Running Locally

**Backend**

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

## Roadmap

- [ ] Fund/cash-flow API routes
- [ ] Dashboard UI (fund table, cash flow chart)
- [ ] Dockerized dev environment
- [ ] CI pipeline
