# Developer Guide

This document provides instructions for developers working on the langnet CLI tool.

## Current Project Status

The langnet CLI tool is a fully functional Python application with the following characteristics:

✅ **Complete Implementation**: CLI tool with langnet API integration  
✅ **Modern Stack**: Click + Rich + sh libraries  
✅ **Reproducible Environment**: Nix/devenv + UV for dependency management  
✅ **Multiple Output Formats**: Rich formatting and JSON output  
✅ **Error Handling**: Robust exception management  
✅ **Task Automation**: Justfile for common commands  
✅ **Package Configuration**: Proper pyproject.toml setup  
✅ **AI Integration**: Opencode agent configuration  

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

# Enter development environment (activates uv automatically)
devenv shell
```

**Important Note:** Devenv uses `uv` for Python environment management, not traditional virtualenvs. There's no need to manually activate virtual environments or set `PYTHONPATH`. The `devenv shell` command handles everything automatically.

### About Opencode Static Analysis Warnings

When working with opencode, you may see import warnings like:
```
ERROR [1:8] Import "click" could not be resolved
ERROR [2:8] Import "sh" could not be resolved
```

**These are normal and expected:**
- They're diagnostic messages from opencode's static analysis tools
- They occur because opencode analyzes code in isolation
- They do NOT indicate actual runtime problems
- The application works perfectly when run properly

**Do NOT try to manually activate environments or set PYTHONPATH for opencode.** The correct workflow is:

```bash
# This is all you need - devenv handles everything
devenv shell
    uv run langcurl --help

# Test that imports work
uv run python -c "import click, sh, rich; print('All dependencies available')"
```

### Verifying the Environment

Once inside `devenv shell`:

```bash
# Check Python environment
echo "Python location: $(which python)"
echo "UV location: $(which uv)"

# Test dependencies (should work)
uv run python -c "import click, sh, rich; print('✅ All dependencies available')"

# Test the application
uv run langcurl --help
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
└── DEV.md            # This developer guide
```

## Code Architecture

### Main Components

1. **CLI Interface** (`langcurl_app/cli.py`)
     - Click command decorators for CLI options
     - Main entry point and argument parsing
     - Output formatting logic
     - Error handling with custom APIError exception

2. **API Client** (`make_api_request()`)
     - HTTP requests to langnet API using `sh` library
     - Error handling and response parsing
     - Curl command construction with proper URL encoding
     - Support for different HTTP status codes

3. **Output Handlers**
     - `format_response()`: Rich-formatted human-readable output
     - JSON output: Machine-parseable JSON strings
     - Debug output to stderr

4. **Environment Management**
     - Nix/devenv for reproducible development
     - UV for Python dependency management
     - Justfile for task automation

### Key Functions

- `make_api_request(query, language)`: Makes HTTP request to langnet API
- `format_response(response)`: Formats JSON response with Rich panels
- `langcurl()`: Main CLI command handler
- `APIError`: Custom exception for API-related errors

### Technical Implementation

- **HTTP Client**: Uses `sh.curl` with proper error handling
- **JSON Processing**: Python's built-in json module
- **CLI Framework**: Click with comprehensive help and options
- **Terminal Formatting**: Rich library for beautiful output
- **Type Hints**: Full type annotations for better code quality
- **Error Handling**: Specific exceptions with detailed error messages

## Development Workflow

### Making Changes

1. **Enter development environment** (if not already):
   ```bash
   devenv shell
   ```

2. **Make your changes** to the source code in `langcurl_app/cli.py`

3. **Test your changes**:
   ```bash
   # Test basic functionality
   just langcurl

   # Test JSON output
   just langcurl-json

   # Test with different parameters
   uv run langcurl --query "test" --language "grc" --json
   ```

### Testing and Verification

The project provides multiple testing approaches:

```bash
# Test all main commands
just langcurl                    # Default search (οὐσία)
just langcurl-greek            # Greek search (φιλεῖν)
just langcurl-latin            # Latin search (amare)
just langcurl-json             # JSON output

# Test error handling
uv run langcurl --query "nonexistent" --language "grc"

# Verify environment
uv run python -c "import click, sh, rich; print('✅ All dependencies available')"

# Build package
uv build
```

### Code Style

- **Python**: Follow PEP 8
- **Imports**: Standard library first, then third-party, then local
- **Error handling**: Use specific exceptions with try/except blocks
- **Type hints**: Use proper type annotations
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Documentation**: Docstrings for all functions and classes

### Dependencies

All dependencies are managed by `devenv` and defined in `devenv.nix` and `pyproject.toml`:

- **Python**: 3.13
- **Click**: CLI framework
- **Rich**: Terminal formatting and colorization
- **sh**: subprocess wrapper
- **uv**: Python package manager
- **hatchling**: Build backend

### Environment Management

**Important:** Devenv uses `uv` for Python package management, not traditional virtualenvs. This means:

- No `.venv/` directories or `activate` scripts
- Dependencies are managed through Nix store paths
- Use `uv run` instead of direct Python execution
- The environment is automatically activated in `devenv shell`

Example workflow:
```bash
# Correct ✅
devenv shell
uv run langcurl --json
uv build

# Incorrect ❌ (no traditional venv to activate)
source .venv/activate  # This doesn't exist
python langcurl_app/cli.py  # Dependencies not found
```

### Build and Package Management

```bash
# Build package within devenv shell
devenv shell
uv build

# Install locally
pip install .

# Check package info
pip show langcurl
```

### Opencode Static Analysis

When using opencode, you may see import warnings. These are normal:

```
ERROR [1:8] Import "click" could not be resolved
```

**These are diagnostic warnings, not runtime errors:**
- Opencode analyzes code in isolation
- The application works fine when run properly
- No manual environment setup needed for opencode
- Focus on runtime testing, not static analysis warnings

**Runtime verification:**
```bash
devenv shell -- uv run python -c "import click, sh, rich; print('Dependencies OK')"
```

## Debugging

### Common Issues

1. **Import Errors**: Ensure you're inside `devenv shell`
   ```bash
   # Check if you're in the right environment
   which python  # Should show devenv's python
   which uv     # Should show devenv's uv
   
   # Test dependencies
   uv run python -c "import click, sh, rich; print('Dependencies OK')"
   ```

2. **API Connection Issues**: The langnet API should be running on localhost:5050
   ```bash
   # Test API connectivity
   curl "http://localhost:5050/api?q=s=test&l=grc"
   ```

3. **Missing Dependencies**: devenv should handle all dependencies automatically
   - If you see import errors, use `uv run` instead of direct `python`
   - Never manually set PYTHONPATH or activate virtualenvs

4. **Build Issues**: Use UV for package building
   ```bash
   devenv shell
   uv build
   ```

### Opencode Import Warnings

**Expected Behavior:**
```
ERROR [1:8] Import "click" could not be resolved
ERROR [2:8] Import "sh" could not be resolved
```

**What to do:**
- Ignore these warnings - they're normal for static analysis
- Test runtime functionality instead:
  ```bash
   devenv shell -- uv run langcurl --help
  ```

**What NOT to do:**
- Don't manually activate virtual environments (they don't exist)
- Don't set PYTHONPATH (it's complex and ineffective)
- Don't worry about static analysis warnings

### Debug Output

Debug information is sent to stderr, while program output goes to stdout:

```bash
# See debug output (stderr)
just langcurl-json

# See only clean JSON (stdout)
just langcurl-json 2>/dev/null

# Capture both separately
just langcurl-json 1>output.json 2>debug.log
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature/my-feature`
6. Submit a pull request

## Deployment

The project uses Nix/devenv for reproducible deployments. The entire development environment, including dependencies, is managed declaratively.

### Production Considerations

- The application expects a running langnet API at localhost:5050
- JSON output is stable and machine-parseable
- Error handling is robust with proper exception management
- No external configuration files required
- Package can be built with `uv build` for distribution

## Troubleshooting

### devenv Issues

If devenv fails to build:

```bash
# Clean the devenv cache
rm -rf .devenv
devenv shell
```

### Python Environment Issues

```bash
# Rebuild the environment
devenv shell --force
```

**Never try to manually fix Python path issues:**
- The devenv + uv combination handles everything automatically
- Manual PYTHONPATH setting is complex and error-prone
- Use `uv run` for all Python execution

### API Issues

If the langnet API is not available:

1. Check if the API service is running on localhost:5050
2. Test connectivity: `curl localhost:5050`
3. Check API logs if available

## Performance Considerations

- The application makes HTTP requests synchronously
- Large JSON responses are handled efficiently with Python's json module
- Terminal output is optimized for readability with Rich formatting
- Memory usage is minimal for typical API responses

## Current Status and Next Steps

### ✅ Completed Features

- **Core CLI Application**: Fully functional langnet API client
- **Multiple Language Support**: Greek (grc) and Latin (lat) searches
- **Dual Output Formats**: Rich formatting and JSON output
- **Robust Error Handling**: Custom exceptions and detailed error messages
- **Environment Management**: Nix/devenv + UV setup
- **Task Automation**: Justfile for common operations
- **Package Configuration**: Proper pyproject.toml with entry points
- **Documentation**: Comprehensive README and developer guide

### 🔄 Current Limitations

- **No Formal Test Suite**: Currently relies on manual testing
- **Single API Endpoint**: Only supports langnet API at localhost:5050
- **No Configuration Files**: All options passed via CLI arguments
- **No Rate Limiting**: No built-in rate limiting for API calls

### 🎯 Potential Enhancements

1. **Testing Framework**
   - Add pytest unit tests
   - Integration tests for API endpoints
   - CLI argument testing

2. **Configuration Management**
   - Support for configuration files
   - Environment variable configuration
   - Custom API endpoint configuration

3. **Enhanced CLI Features**
   - Batch processing capabilities
   - Output format customization
   - Progress indicators for long operations

4. **API Improvements**
   - Retrying failed requests
   - Rate limiting
   - Connection timeout handling
   - Support for multiple API endpoints

5. **Packaging Distribution**
   - Publish to PyPI
   - Docker containerization
   - GitHub Actions CI/CD pipeline

### 📊 Development Metrics

- **Code Quality**: Full type hints, proper error handling
- **Documentation**: Comprehensive docs and examples
- **Reproducibility**: Nix/devenv environment
- **Testing**: Manual testing via just commands
- **Dependencies**: Minimal, well-managed dependencies
- **Code Size**: ~150 lines of core application code
