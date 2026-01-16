# AGENTS.md

## Project Overview
Nix/devenv-based development environment with Click-based Python langcurl app with langnet API integration. Configuration is declarative via Nix expressions.

## Code Structure
```
.
├── langcurl_app/     # Python application directory
│   ├── __init__.py
│   └── cli.py        # Main CLI application
├── justfile         # Just task runner recipes
├── devenv.nix       # Development environment configuration
├── AGENTS.md        # AI assistant configuration
├── README.md        # User documentation
└── DEV.md           # Developer guide
```

## Commands
- `devenv shell just` - Run default task (langcurl app with Greek API search)
- `devenv shell just -- langcurl` - Run langcurl app with default settings
- `devenv shell just -- langcurl-greek` - Search langnet API for Greek text (φιλεῖν)
- `devenv shell just -- langcurl-latin` - Search langnet API for Latin text (amare)
- `devenv shell just -- langcurl-json` - Search langnet API and output parsable JSON
- `devenv shell bash -- -c "$somebash"` - Run bash script inside of devenv

## Code Style
- **Python**: Use Click for CLI, `sh` library for subprocess calls, `rich` for pretty printing
- **Nix**: 2-space indentation, kebab-case attributes, double quotes
- **Imports**: Standard library first, then third-party, then local
- **Error handling**: Use try/except blocks with specific exceptions
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Type hints**: Use proper type annotations for function parameters and returns

## Build/Test
- `devenv shell just -- $justcmd` - Run $justcmd inside devenv shell.
- `devenv shell uv -- build` - Build package (run within devenv shell)
- No formal test framework configured yet

## CLI Options
- `--query TEXT`: Text to search in langnet database (default: οὐσία)
- `--language TEXT`: Language code (grc/lat, default: grc)
- `--json`: Output parsable JSON instead of formatted output
