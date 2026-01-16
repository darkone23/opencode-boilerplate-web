import click
import sh
from sh import curl
import json
import sys
from typing import Optional, Dict, Any
from rich.console import Console
from rich.pretty import Pretty
from rich.panel import Panel

console = Console()


class APIError(Exception):
    """Custom exception for API-related errors."""
    pass


def make_api_request(query: str, language: str) -> Dict[str, Any]:
    """
    Make API request to the langnet service.
    
    Args:
        query: The text to search for
        language: The language code (e.g., 'grc' for Greek)
        
    Returns:
        Parsed JSON response
        
    Raises:
        APIError: If the API request fails or response cannot be parsed
    """
    try:
        print(f"Making API request for query: '{query}' (language: {language})...", file=sys.stderr)
        
        result = curl(
            "--data-urlencode", f"s={query}",
            "--data-urlencode", f"l={language}", 
            "--get", "http://localhost:5050/api/q",
            _ok_code=[0, 200, 400],
            _err_to_out=True  # Include stderr in stdout for better error handling
        )
        
        # Check if result is a string (success) or CompletedProcess object
        if hasattr(result, 'exit_code'):
            print(f"curl exit code: {result.exit_code}", file=sys.stderr)
            stdout = result.stdout
        else:
            print("curl command succeeded", file=sys.stderr)
            stdout = result
        
        if not stdout.strip():
            raise APIError("Empty response from API")
        
        try:
            response_data = json.loads(stdout)
            return response_data
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}", file=sys.stderr)
            print("Raw response:", file=sys.stderr)
            print(stdout, file=sys.stderr)
            raise APIError(f"Failed to parse JSON response: {e}")
            
    except sh.ErrorReturnCode as e:
        error_msg = f"API request failed with exit code {e.exit_code}"
        if e.stdout:
            try:
                error_response = json.loads(e.stdout)
                error_msg += f". Response: {json.dumps(error_response, indent=2)}"
            except json.JSONDecodeError:
                error_msg += f". Raw output: {e.stdout}"
        else:
            error_msg += ". No output available"
        
        print(error_msg, file=sys.stderr)
        raise APIError(error_msg)


def format_response(response: Dict[str, Any]) -> Panel:
    """
    Format the API response for display.
    
    Args:
        response: The parsed JSON response
        
    Returns:
        Rich Panel object for display
    """
    # Create formatted content
    content = Pretty(response)
    
    return Panel(
        content,
        title="langnet API Response",
        border_style="blue",
        padding=(1, 2)
    )


@click.command()
@click.option(
    "--query", 
    default="οὐσία", 
    help="Text to search in the langnet database",
    show_default=True
)
@click.option(
    "--language", 
    default="grc", 
    help="Language code for the search (e.g., 'grc' for Greek, 'lat' for Latin)",
    show_default=True
)
@click.option(
    "--json", 
    "json_output", 
    is_flag=True, 
    help="Output parsable JSON instead of formatted output"
)
def langcurl(query: str, language: str, json_output: bool) -> None:
    """
    A CLI application that performs langnet API searches.
    
    This application integrates with the langnet digital library API for
    classical language text analysis.
    """
    
    # Make API request
    try:
        response_data = make_api_request(query, language)
        
        if json_output:
            # Show raw JSON
            console.print(json.dumps(response_data, indent=2, ensure_ascii=False))
        else:
            # Show formatted response
            formatted_panel = format_response(response_data)
            console.print(formatted_panel)
            
    except APIError as e:
        print(f"Error: {e}", file=sys.stderr)
        raise click.ClickException(str(e))
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        raise click.ClickException(f"Unexpected error: {e}")


if __name__ == "__main__":
    langcurl()
