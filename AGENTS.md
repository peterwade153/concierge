## Project Domain

A Restaurant Recommendation Agent, that recommends fine dining spots in specific neighborhood. 
Uses Nominatim API to get Location Coordinates, and FourSquare API to look up restaurants within a radius of those Coordinates.

## Project Setup and Management

- Python version: 3.11.
- Dependency management: `pip` and `backend/requirements.txt` file.
- Add a dependency with `pip install <package>`.
- Run the app with `python backend/api/run.py`.
- Run backend tests with `pytest` (works from the repo root or inside `backend/`,
  thanks to `backend/conftest.py`).
- Run frontend tests with `npm test` (inside `frontend/`).
- Run the full stack (backend + React frontend) with `docker compose up --build`.
- Branch from `master` as `feature/<name>` and use Conventional Commits.
- Stage changes for review. Don't commit to `master` or push without being asked.

## Architecture Overview

- **backend/** : Python application — the AI restaurant recommendation agent (`agent/`) and the FastAPI REST API (`api/`).
  - `backend/Dockerfile` builds this image; the compose context is `./backend`.
- **frontend/** : React + Vite + TypeScript SPA served by nginx in production.
  - `frontend/Dockerfile` builds this image; the compose context is `./frontend`.
- **docker-compose.yml** : orchestrates the backend and frontend containers.
  - API keys come from `.env` at the repo root via `env_file`; never bake them in.

## API

- `POST /api/recommend` with body `{"query": "..."}` returns
  `{"recommendation": {"neighborhood_searched", "recommended_spots", "summary_verdict"}}`.
- 500 on agent construction failure, 502 when the agent returns no recommendation.
- Successful results are cached (max 128); failures are not cached, so they are retryable. 

## Coding Conventions

- Type-hint public functions and methods, including their return types.
- Use `pathlib` for path management. Don't use `os.path`.
- Prefer f-strings over `str.format()` or `%` formatting.
- Follow EAFP: handle exceptions rather than checking conditions up front.
- Write Google-style docstrings for every public function and method.
- Validate request bodies with Pydantic models.
- Embrace idiomatic Python like comprehensions, generators, and decorators.
- Lint before declaring a task done: `ruff check backend` and
  `cd frontend && npm run lint`.

## CI

A GitHub Actions workflow at `.github/workflows/ci.yml` runs on every push
and pull request. It installs dependencies, lints, type-checks, and runs the
test suites for both the backend (`pytest`) and the frontend (`npm test`).

## Constraints

- Ask before adding any external dependency.
- Preserve the signature and response shape of existing endpoints.
- Don't use blocking I/O inside `async` functions.
- Keep existing tests intact, and fix the code to make them pass.
- Declare a task done only after the gates pass and docstrings are
  updated.

## Ignore

Treat everything in `.gitignore` as off-limits to read or edit. On top of
that, never open:

- Secrets and `.env` files
- Large data files unrelated to the current task
- Vendored or generated code
