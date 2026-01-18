# Developer Guide

This document provides instructions for developers working on this full-stack web application template.

## Current Project Status

This is a fully functional full-stack web application template with the following characteristics:

- **Frontend**: Vite + TypeScript + Tailwind CSS + DaisyUI + HTMX + Surreal.js
- **Backend**: Flask + Blueprint routes + Jinja2 + Gunicorn
- **CLI**: Click + Rich + sh libraries
- **Data Processing**: Polars + DuckDB + cattrs
- **Environment**: Nix/devenv + UV (Python) + Bun (JavaScript)
- **Task Automation**: Just (justfiles in root, backend, and frontend)

## Development Environment Setup

### Prerequisites

- [Nix](https://nixos.org/download/)
- [devenv](https://devenv.sh/)
- [Git](https://git-scm.com/)

### Environment Activation

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Enter development environment
devenv shell

# Install frontend dependencies
cd frontend && bun install && cd ..

# Enter developer zellij session (optional but recommended)
just devenv-zell
```

**Important Note:** Devenv manages both Python (via UV) and JavaScript (via Bun) environments automatically. There's no need to manually activate virtual environments or install global packages.

### Verifying the Environment

```bash
# Check all tools are available
which python    # Should show devenv's python
which uv        # Should show devenv's uv
which bun       # Should show devenv's bun
which node      # Should show devenv's node

# Test Python dependencies
uv run python -c "import flask, click, rich, duckdb, polars, cattrs; print('Python deps OK')"

# Test frontend dependencies
cd frontend && bun run build && cd ..
```

## Project Structure

```
.
├── frontend/                   # Frontend application
│   ├── src/
│   │   ├── main.ts            # Application entry point
│   │   └── tailwind.css       # Tailwind + DaisyUI imports
│   ├── public/                # Static assets
│   ├── index.html             # HTML entry point
│   ├── vite.config.ts         # Vite configuration
│   ├── tsconfig.json          # TypeScript configuration
│   ├── postcss.config.js      # PostCSS configuration
│   ├── package.json           # Frontend dependencies
│   ├── bun.lock               # Bun lockfile
│   └── justfile               # Frontend commands
├── backend/                    # Backend application
│   ├── boilerplate_app/
│   │   ├── web/
│   │   │   ├── __init__.py    # Flask app factory
│   │   │   ├── routes.py      # API Blueprint routes
│   │   │   └── templates/     # Jinja2 templates
│   │   ├── __init__.py
│   │   ├── cli.py             # CLI application
│   │   ├── wsgi.py            # WSGI entry point
│   │   ├── cattrs_example.py  # Cattrs examples
│   │   ├── duckdb_example.py  # DuckDB examples
│   │   └── polars_example.py  # Polars examples
│   ├── pyproject.toml         # Python package config
│   ├── uv.lock                # UV lockfile
│   └── justfile               # Backend commands
├── devenv.nix                  # Nix development environment
├── devenv.yaml                 # Devenv inputs
├── devenv.lock                 # Devenv lockfile
├── justfile                    # Root task runner
├── .envrc                      # Direnv configuration
├── .gitignore                  # Git ignore rules
├── AGENTS.md                   # AI assistant configuration
├── README.md                   # User documentation
├── DEV.md                      # This developer guide
└── INSTRUCTIONS.md             # Migration tracking
```

## Development Workflow

### Starting Development Servers

```bash
# Start both frontend and backend (recommended)
just dev

# Or start them separately in different terminals:
just dev-frontend    # Vite at http://localhost:43210
just dev-backend     # Flask at http://localhost:43280
```

The Vite dev server proxies all `/api/*` requests to Flask, so you can develop the full stack from `http://localhost:43210`.

### Making Frontend Changes

1. Edit files in `frontend/src/`
2. Changes hot reload automatically
3. Tailwind classes are processed on-the-fly
4. TypeScript errors show in the browser console

```bash
# Frontend-specific commands
cd frontend
bun run dev      # Start dev server
bun run build    # Build for production
bun run preview  # Preview production build
```

### Making Backend Changes

1. Edit files in `backend/boilerplate_app/`
2. Flask dev server auto-reloads on file changes
3. Test API endpoints at `http://localhost:43280/api/*`

```bash
# Backend-specific commands (from backend/ directory)
just dev         # Start Flask dev server
just run-server  # Start gunicorn production server
just run-cli     # Run CLI application
```

### Adding API Endpoints

Edit `backend/boilerplate_app/web/routes.py`:

```python
from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

@api.route('/my-endpoint', methods=['GET'])
def my_endpoint():
    return jsonify({'data': 'value'})

@api.route('/my-htmx-endpoint', methods=['GET'])
def my_htmx_endpoint():
    """Return HTML partial for HTMX"""
    return '<div class="alert alert-info">Hello from HTMX!</div>'
```

### Adding Frontend Interactivity

Use HTMX for server-driven updates:

```html
<button hx-get="/api/my-htmx-endpoint" hx-target="#result">
  Load Content
</button>
<div id="result"></div>
```

## Building for Production

```bash
# Build frontend
just build

# The built files are output to frontend/dist/
# Flask serves these automatically in production mode

# Start production server
just run
```

## Code Architecture

### Frontend Components

| File | Purpose |
|------|---------|
| `index.html` | HTML entry point with app mount |
| `src/main.ts` | Application initialization, HTMX setup |
| `src/tailwind.css` | Tailwind CSS + DaisyUI imports |
| `vite.config.ts` | Dev server, proxy, build configuration |

### Backend Components

| File | Purpose |
|------|---------|
| `web/__init__.py` | Flask app factory, static file serving |
| `web/routes.py` | API Blueprint with route handlers |
| `wsgi.py` | WSGI entry point for gunicorn |
| `cli.py` | Click-based CLI application |

### Request Flow

```
Development:
  Browser → Vite (43210) → [static files]
                        → /api/* → Flask (43280)

Production:
  Browser → Gunicorn (43280) → [static from dist/]
                             → /api/* → Flask routes
```

## Code Style

### Python
- Use Flask Blueprints for route organization
- Return `jsonify()` for JSON endpoints
- Return HTML strings for HTMX endpoints
- Use type hints for function parameters and returns
- Follow PEP 8 naming conventions

### TypeScript
- Use strict mode (configured in tsconfig.json)
- Import HTMX and initialize in main.ts
- Use Tailwind/DaisyUI classes for styling

### Nix
- 2-space indentation
- kebab-case for attribute names
- Double quotes for strings

## Testing

### Manual Testing

```bash
# Test full stack
just dev
# Visit http://localhost:43210

# Test API directly
curl http://localhost:43280/api/hello
curl http://localhost:43280/api/hello-htmx

# Test CLI
just run-cli
just run-json
```

### Demo Commands

```bash
just demo-duckdb    # DuckDB query examples
just demo-polars    # Polars DataFrame examples
just demo-cattrs    # Cattrs serialization examples
```

## Troubleshooting

### Frontend Issues

**Vite won't start:**
```bash
cd frontend
bun install    # Reinstall dependencies
bun run dev    # Try again
```

**Tailwind styles not applying:**
- Ensure `@import "tailwindcss"` is in `tailwind.css`
- Ensure `@plugin "daisyui"` is in `tailwind.css`
- Check that `tailwind.css` is imported in `main.ts`

**HTMX not working:**
- Check browser console for errors
- Ensure `htmx.org` is imported in `main.ts`
- Verify API endpoint returns HTML (not JSON) for HTMX targets

### Backend Issues

**Import errors:**
```bash
# Ensure you're in devenv shell
devenv shell

# Use uv run for Python execution
uv run python -c "import flask; print('OK')"
```

**Flask won't start:**
```bash
cd backend
just dev    # Check error output
```

**API proxy not working:**
- Ensure Flask is running on port 43280
- Check Vite proxy config in `vite.config.ts`
- Look for CORS errors in browser console

### Environment Issues

**devenv fails to build:**
```bash
rm -rf .devenv
devenv shell
```

**Dependencies out of sync:**
```bash
# Python
cd backend && uv sync && cd ..

# JavaScript
cd frontend && bun install && cd ..
```

## Ports Reference

| Service | Port | Purpose |
|---------|------|---------|
| Vite | 43210 | Frontend dev server |
| Flask | 43280 | Backend API server |

## Adding Dependencies

### Python Dependencies

```bash
cd backend
uv add <package-name>
```

### JavaScript Dependencies

```bash
cd frontend
bun add <package-name>        # Runtime dependency
bun add -d <package-name>     # Dev dependency
```

## Next Steps

### Potential Enhancements

1. **Testing**: Add pytest (backend) and vitest (frontend)
2. **Authentication**: Add Flask-Login or JWT
3. **Database**: Add SQLAlchemy or continue with DuckDB
4. **Deployment**: Add Docker configuration
5. **CI/CD**: Add GitHub Actions workflow
