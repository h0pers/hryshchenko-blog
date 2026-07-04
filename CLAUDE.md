# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

### Common commands

```bash
# Local dev with hot reload (mounts ./website into the container)
docker compose -f docker-compose.debug.yml up --build

# Build the dev-target image once (only needed when deps change)
docker build --target development -t backend:test .

# Full test suite (pytest + coverage via website/pytest.sh)
docker compose -f docker-compose.test.yml run --rm test

# Single test file
docker compose -f docker-compose.test.yml run --rm test pytest apps/core/tests/test_something.py

# Full suite with coverage report + XML (as CI does)
docker compose -f docker-compose.test.yml run --rm test ./pytest.sh --ci

# Lint/format (ruff)
uvx ruff check .
uvx ruff format .

# Frontend run from frontend/
npm run lint
npm run lint:fix
npm run format
npm run build
```

Production is smoke-tested locally with `docker compose up` (pulls the pre-built GHCR image; does not build from source).

### Settings architecture (django-split-settings)

`website/website/settings/__init__.py` is the actual `DJANGO_SETTINGS_MODULE`. It reads `DJANGO_ENV` (`development` / `production` / `test`, default `production`) and stitches settings together with `split_settings.tools.include`:

1. `components/*.py` — shared building blocks (`base`, `database`, `security`, `email`, `logging`, `cache`, plus `rest_framework`/`cors` if `use_drf`, `wagtail` if `use_wagtail`, `vite` if `use_vue`). Included unconditionally in this fixed order.
2. `environments/{development,production,test}.py` — included last, so it can override or append to anything a component defined (e.g. `production.py` does `MIDDLEWARE.append(...)`).

Because these files are `include()`d into one shared namespace rather than imported as modules, names like `MIDDLEWARE`, `BASE_DIR`, or `env` are available in later files without importing them — don't add imports for names defined in an earlier component/environment file (ruff's per-file-ignores already silences `F821` for these directories for this reason).

### App layout

- `apps/core` — cross-cutting: health check API (`api/`), the production-only secure-headers middleware (`middleware.py`), and the one settings-mode test (`tests/test_django_mode.py`).
- `apps/cms` — Wagtail pages/templates

### Docker build

`Dockerfile` is a multi-stage build: a shared `base` (uv + Python 3.11 Alpine) branches into `deps` (prod deps only) / `deps-dev` (all deps) and a shared `runtime` stage, producing final `development` and `production` targets. An additional `frontend-build` Node stage runs `npm run build` and its output (`static/dist`) is copied only into the `production` target — `development` relies on Vite's dev server instead (see `DJANGO_VITE["default"]["dev_mode"] = True` in `environments/development.py`).

### CI/CD (generated project)

- `ci.yml` — builds the `development` Docker target and runs `docker-compose.test.yml` on every push/PR.
- `deploy.yml` — triggered by a successful CI run on `master`; builds+pushes the `production` image to GHCR, writes a `.env` from GitHub secrets, scp's it + `docker-compose.yml` to the VPS, then runs migrations and a `docker rollout` for zero-downtime restart.
- `pre-commit.yml` — runs the ruff pre-commit hooks.
- Per-server `GUNICORN_WORKERS`/`GUNICORN_TIMEOUT` are deliberately *not* templated into CI — they're set via a `docker-compose.override.yml` the operator creates directly on the VPS (see the generated project's `README.md`).

### Code style

Ruff is configured in `pyproject.toml` (`target-version = py311`, rule set includes Django-specific `DJ` checks, `T20` bans stray prints, `dummy-variable-rgx` allows underscore-prefixed unused vars). `migrations` and `static` are excluded from linting.
