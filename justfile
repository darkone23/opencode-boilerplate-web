default:
    uv run langcurl

langcurl:
    uv run langcurl --query "οὐσία" --language "grc"

langcurl-greek:
    uv run langcurl --query "φιλεῖν" --language "grc"

langcurl-latin:
    uv run langcurl --query "amare" --language "lat"

langcurl-json:
    uv run langcurl --query "οὐσία" --language "grc" --json
