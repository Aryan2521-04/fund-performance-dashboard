# Fund Performance Dashboard

A full-stack app for tracking private equity / VC fund cash flows and computing standard performance metrics — IRR, TVPI, and DPI — from contribution, distribution, and NAV data.

**Status:** DONE

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

**Tests**

````bash
cd backend
source venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest tests/test_api.py tests/test_metrics.py
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
````

**With Docker**

```bash
docker compose up --build
```

**First run only**

```bash
docker compose run --rm backend python -m app.seed_data
```

## Roadmap

- [ ] Bug fixes

## Known Issues / TODO

### Bugs

- [ ] `CashFlowChart.jsx`: `.sort()` mutates React state in place; copy the array first (`[...cash_flows].sort(...)`)
- [ ] `App.jsx`: fund detail fetch has a race condition when switching funds quickly; add an `ignore` cleanup flag

### Testing / Infra

- [ ] Add tests for `fund_service.compute_fund_metrics`

### Robustness

- [ ] Frontend has no error or loading state when the API call fails

### Cleanup

- [ ] Use `selectinload` in `get_funds` to avoid N+1 queries as the number of funds grows
- [ ] Refactor the three repeated fetch functions in `api.js` into one shared `request()` helper
- [ ] Chart X axis: use a time/numeric scale so points are spaced by actual date
- [ ] Table rows: add a pointer cursor, a selected-row highlight and keyboard access
- [ ] Rename `package.json` from `vite-react-starter`
- [ ] Make `test_irr_with_nav` check against `xirr()` instead of only `>` comparisons
