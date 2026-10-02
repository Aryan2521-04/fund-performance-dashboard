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

- [ ] Dockerized dev environment
- [ ] CI pipeline

## Known Issues / TODO

### Bugs

- [ ] `models.py`: `nav_snapshots` and `cash_flows` relationships have no `order_by`, so `fund_service` grabs the last-inserted NAV instead of the
      latest-dated one
- [ ] `seed_data.py`: never calls `Base.metadata.create_all()`, so it crashes on a fresh database
- [ ] `CashFlowChart.jsx`: `.sort()` mutates React state in place; copy the array first (`[...cash_flows].sort(...)`)
- [ ] `App.jsx`: fund detail fetch has a race condition when switching funds quickly; add an `ignore` cleanup flag

### Testing / Infra

- [ ] `tests/test_api.py` is empty; add `TestClient` tests for `GET /funds`, `GET /funds/{id}` and `POST /funds/{id}/cashflows` (needs `httpx`)
- [ ] Add tests for `fund_service.compute_fund_metrics`
- [ ] `ci.yml`, `docker-compose.yml` and both Dockerfiles are empty

### Robustness

- [ ] `database.py`: SQLite path is relative, so it creates a different DB depending on where uvicorn is started; build it from `Path(__file__)`
- [ ] Frontend has no error or loading state when the API call fails
- [ ] `calculate_irr_with_nav` should check that the NAV date is on or after the last cash flow, so NAV isn't counted twice
- [ ] Move the hardcoded API URL in `api.js` to `import.meta.env.VITE_API_URL`

### Cleanup

- [ ] Remove unused imports: `models` and `metrics` in `routers/funds.py`, `Decimal` in `fund_service.py`, `CartesianGrid` and `Tooltip` in
      `CashFlowChart.jsx` (or use `Tooltip`)
- [ ] Delete the duplicated metrics loop in `seed_data.py`'s `__main__` block, along with its now-unused metric imports
- [ ] Fix typos in API error messages ("dosen't", "datbase") in `routers/funds.py`
- [ ] Turn off `echo=True` in `database.py`, or control it with an env var
- [ ] Add the `Session` type hint to `crud.get_funds(db)`
- [ ] Use `selectinload` in `get_funds` to avoid N+1 queries as the number of funds grows
- [ ] Refactor the three repeated fetch functions in `api.js` into one shared `request()` helper
- [ ] Chart X axis: use a time/numeric scale so points are spaced by actual date
- [ ] Table rows: add a pointer cursor, a selected-row highlight and keyboard access
- [ ] Rename `package.json` from `vite-react-starter`
- [ ] Split `requirements.txt` into runtime and dev (`pytest`, `pyxirr`) files
- [ ] Make `test_irr_with_nav` check against `xirr()` instead of only `>` comparisons
