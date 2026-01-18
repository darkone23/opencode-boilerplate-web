# Backend

Flask-based backend with CLI tools, serving both API endpoints and the production frontend.

## Structure

```
backend/
├── boilerplate_app/
│   ├── web/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── routes.py          # API Blueprint routes
│   │   └── templates/         # Jinja2 templates
│   ├── __init__.py
│   ├── cli.py                 # CLI application (Click + Rich)
│   ├── wsgi.py                # WSGI entry point
│   ├── cattrs_example.py      # Cattrs serialization demos
│   ├── duckdb_example.py      # DuckDB query demos
│   └── polars_example.py      # Polars DataFrame demos
├── pyproject.toml             # Python package configuration
├── uv.lock                    # UV dependency lockfile
└── justfile                   # Backend-specific commands
```

## Commands

```bash
# From backend/ directory
just dev          # Start Flask dev server (port 43280)
just run-server   # Start gunicorn production server
just run-cli      # Run CLI application
just run-custom   # Run CLI with custom message
just run-json     # Run CLI with JSON output
just demo-duckdb  # Run DuckDB demonstration
just demo-polars  # Run Polars demonstration
just demo-cattrs  # Run cattrs demonstration
just uv-sync      # Sync Python dependencies
```

## API Endpoints

| Endpoint | Method | Response | Description |
|----------|--------|----------|-------------|
| `/api/hello` | GET | JSON | Returns `{"message": "Hello from Flask API!"}` |
| `/api/hello` | POST | JSON | Returns personalized greeting with `name` from body |
| `/api/hello-htmx` | GET | HTML | Returns HTML partial for HTMX consumption |

## Adding New Endpoints

Edit `boilerplate_app/web/routes.py`:

```python
@api.route('/my-endpoint', methods=['GET'])
def my_endpoint():
    return jsonify({'key': 'value'})

@api.route('/my-htmx-endpoint', methods=['GET'])
def my_htmx_endpoint():
    """Return HTML for HTMX targets"""
    return '<div class="alert">Content here</div>'
```

## Dependencies

Managed via `pyproject.toml` with UV:

- **flask**: Web framework
- **gunicorn**: Production WSGI server
- **jinja2**: Templating engine
- **click**: CLI framework
- **rich**: Terminal formatting
- **sh**: Subprocess wrapper
- **polars**: DataFrame library
- **duckdb**: In-memory SQL database
- **cattrs**: Dataclass serialization

## Production

In production, Flask serves the built frontend from `frontend/dist/`:

```bash
# Build frontend first (from root)
just build

# Start production server
just run-server
```
