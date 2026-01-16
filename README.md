# langnet CLI Tool

A Python CLI application that integrates with the langnet digital library API for classical language text analysis.

## Features

- Search Greek and Latin text in the langnet database
- Clean JSON output for programmatic use (compatible with jq, nushell, etc.)
- Formatted human-readable output with Rich
- Built with Click for CLI interface
- Nix/devenv environment for reproducible development

## Quick Start

### Prerequisites
- [Nix](https://nixos.org/download/)
- [devenv](https://devenv.sh/)

### Setup and Run

```bash
# Enter development environment (all setup is automatic)
devenv shell

# Run default search
just

# Run specific searches
just langcurl-greek    # Search for Greek: φιλεῖν
just langcurl-latin    # Search for Latin: amare
just langcurl-json     # Clean JSON output

# Direct usage
uv run langcurl --help
uv run langcurl --query "φιλοσοφία" --language "grc" --json
```

## CLI Options

- `--query TEXT`: Text to search in langnet database (default: οὐσία)
- `--language TEXT`: Language code (grc/lat, default: grc)  
- `--json`: Output parsable JSON instead of formatted output

## Examples

### JSON Output for Scripting

```bash
# Clean JSON output perfect for piping to jq
just langcurl-json | jq '.diogenes.chunks[0].chunk_type'

# Output to file
just langcurl-json > results.json
```

### Different Languages

```bash
# Greek search
uv run langcurl --query "φιλοσοφία" --language "grc"

# Latin search  
uv run langcurl --query "amare" --language "lat"
```

## Project Structure

```
.
├── langcurl_app/     # Python application directory
│   ├── __init__.py
│   └── cli.py        # Main CLI application
├── justfile          # Just task runner recipes
├── devenv.nix        # Development environment configuration
├── devenv.yaml       # Alternative devenv configuration
├── pyproject.toml    # Python package configuration
├── uv.lock           # UV dependency lockfile
├── devenv.lock       # Devenv environment lockfile
├── .envrc            # Environment variables
├── AGENTS.md         # AI assistant configuration
├── README.md         # User documentation
└── DEV.md            # Developer guide
```

## Architecture

- **CLI Layer**: Click-based command interface
- **HTTP Client**: `sh` library for curl requests
- **Output**: Rich for formatted display, JSON for machine consumption
- **API**: langnet digital library REST API
- **Environment**: Nix/devenv for reproducible development
- **Package Manager**: UV for Python dependency management

## Development

See [DEV.md](./DEV.md) for developer instructions and contribution guidelines.

## License

MIT
