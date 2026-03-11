# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Task Manager app built for testing CI/CD pipelines with Kubernetes. Flask backend + Quasar/Vue 3 frontend, both containerized.

## Build & Run Commands

### Backend
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run dev server
python backend/app.py

# Run with gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 app:app --chdir backend
```

### Frontend
```bash
# Install dependencies
cd frontend && npm install

# Dev server (port 9000, proxies /api to localhost:5000)
cd frontend && npx quasar dev

# Production build
cd frontend && npx quasar build

# Lint
cd frontend && npm run lint
```

### Docker
```bash
# Build and run both services
docker-compose up --build

# Backend only: localhost:5000, Frontend only: localhost:8080
```

### Tests
```bash
# Run all backend tests
pytest backend/test_app.py

# Run a single test
pytest backend/test_app.py::test_health

# Verbose output
pytest backend/test_app.py -v
```

No frontend tests are configured.

## Architecture

Two-container microservice: frontend (Nginx serving Quasar SPA) proxies `/api/` requests to backend (Flask behind gunicorn).

- **Backend** (`backend/app.py`): Flask REST API with in-memory task store. All routes under `/api/`. The `/api/health` endpoint returns `APP_VERSION` env var — this is the key mechanism for canary deployment testing.
- **Frontend** (`frontend/src/`): Quasar 2 + Vue 3 Composition API. Axios instance in `src/boot/axios.js` uses baseURL `/api`. Layout fetches backend version for display in header badge.
- **Nginx** (`frontend/nginx.conf`): Serves SPA with `try_files` fallback, proxies `/api/` to `flask-backend:5000` (K8s Service DNS name in production, Docker Compose service name locally).

### API Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| GET | /api/health | Health check + version |
| GET | /api/tasks | List all tasks |
| POST | /api/tasks | Create task (body: `{title}`) |
| PATCH | /api/tasks/:id | Update task (body: `{title?, done?}`) |
| DELETE | /api/tasks/:id | Delete task |

### Frontend Dev Proxy
`quasar.config.js` proxies `/api` to `http://localhost:5000` during development, so run the Flask backend on port 5000 alongside `quasar dev`.

---

## Current Goal: Interview Prep + Hands-On Lab

**Target job:** Richwell Senior SRE (see `/home/ops/albert_code/k8s/i_want_to_land_this_job.txt`)

**What I'm building:** Full CI/CD + GitOps + Canary pipeline using this Task Manager app as the demo project.

**Learning guide:** See `/home/ops/albert_code/k8s/write_to_this_folder/argocd-gitops-cicd-canary.md` for concepts.

**Implementation roadmap + interview prep:** See `/home/ops/albert_code/k8s/write_to_this_folder/interview-prep-implementation-plan.md` for step-by-step phases and expected interview questions.

### Implementation Phases (in order)
1. **k3d cluster** — create local K8s cluster with registry
2. **Helm chart** — templatize backend + frontend into Helm
3. **Manual deploy** — build images, import to k3d, helm install
4. **Argo CD** — install, create Application CRD, GitOps sync
5. **Config repo** — two-repo pattern (app repo + config repo)
6. **CI pipeline** — automate test → build → push → update config repo
7. **Argo Rollouts** — canary deployment with traffic shifting

### Key Design Decisions
- `/api/health` returns `APP_VERSION` env var — this is how we verify canary is working (mixed v1/v2 responses during rollout)
- Helm `values.yaml` image tag is the single value CI/CD changes on each deploy
- Two-repo pattern: this repo is the "app repo" (CI watches it), a separate config repo holds Helm charts (Argo CD watches it)
- Pull model: Argo CD inside cluster pulls from Git, no external kubectl access needed
