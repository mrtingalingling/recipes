## API and MCP Integration Guide

This guide explains how to use the new API and MCP modules in the recipes application.

### Directory Structure

```
backend/
├── api/                 # External API client implementations
│   ├── __init__.py
│   ├── client.py       # Generic API client wrapper
│   └── auth.py         # Authentication manager
├── mcp/                 # Model Context Protocol server
│   ├── __init__.py
│   └── server.py       # MCP server implementation
└── utils/              # Shared utilities
    ├── __init__.py
    ├── http.py         # HTTP helpers
    └── validators.py   # Input validation
```

---

## Using the API Client

### Basic Usage

```python
from backend.api.client import APIClient
from backend.api.auth import APIAuthManager

# Initialize auth manager
async def refresh_token(user_id: str):
    """Custom token refresh logic."""
    # Call your token refresh endpoint
    return new_token, new_refresh_token, expires_in

auth_manager = APIAuthManager(refresh_func=refresh_token)

# Create API client
async with APIClient("https://api.example.com", auth_manager) as client:
    # Make authenticated GET request
    recipes = await client.get("recipes", user_id="user123", params={"limit": 10})
    
    # Make authenticated POST request
    result = await client.post(
        "meal-plans",
        user_id="user123",
        data={"budget": 100, "preferences": ["vegetarian"]}
    )
```

### Integration with Existing Code

The API client integrates seamlessly with the existing `token_manager.py`:

```python
from backend.token_manager import get_token, refresh_access_token

async def my_refresh_func(user_id: str):
    """Refresh token using token_manager."""
    new_token = refresh_access_token(
        user_id,
        lambda rt: requests.post("https://api.example.com/refresh", json={"refresh_token": rt}).json()
    )
    return new_token, None, 3600  # 1 hour expiry
```

---

## Using the MCP Server

### Starting the Server

```bash
# Start in production mode
make mcp-server

# Start in development mode (with auto-reload)
make mcp-dev

# Or manually
python -m backend.mcp.server
```

### Registering Custom Tools

Edit `backend/mcp/server.py` to add your own tools:

```python
def _register_tools(self):
    """Register MCP tools for Claude interaction."""
    self.tools = {
        "my_custom_tool": {
            "description": "What this tool does",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "param1": {"type": "string"},
                },
            },
        },
    }
```

### Handling Tool Calls

Implement `handle_tool_call` to execute your tools:

```python
async def handle_tool_call(self, tool_name: str, params: Dict[str, Any]) -> Any:
    """Handle tool calls from Claude."""
    if tool_name == "my_custom_tool":
        result = await self.my_custom_tool_impl(params["param1"])
        return result
```

---

## Using Utility Functions

### HTTP Helpers

```python
from backend.utils.http import HTTPHelper

# Create standardized responses
success = HTTPHelper.success_response(
    data={"recipes": [...]},
    message="Recipes fetched successfully"
)

error = HTTPHelper.error_response(
    "Budget must be greater than 0",
    status_code=400
)
```

### Input Validation

```python
from backend.utils.validators import (
    validate_budget,
    validate_dietary_preferences,
    validate_servings
)

# Use in FastAPI endpoints
from fastapi import FastAPI, HTTPException

@app.post("/meal-plans")
async def create_meal_plan(budget: float, preferences: list):
    try:
        validate_budget(budget)
        validate_dietary_preferences(preferences)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Create meal plan...
```

---

## Integration with FastAPI

### Option 1: Mount MCP as FastAPI Routes

```python
# backend/api_server.py
from fastapi import FastAPI
from backend.mcp.server import MCPServer

app = FastAPI()
mcp_server = MCPServer()

@app.get("/mcp/tools")
async def get_mcp_tools():
    """Get list of available MCP tools."""
    return mcp_server.tools

@app.post("/mcp/call")
async def call_mcp_tool(tool_name: str, params: dict):
    """Call an MCP tool."""
    return await mcp_server.handle_tool_call(tool_name, params)
```

### Option 2: Run MCP as Separate Process

```bash
# Start API server
make dev

# In another terminal, start MCP server
make mcp-server
```

---

## Testing

### Run API Client Tests

```bash
make api-test
```

Test file: `tests/test_api_client.py`

### Run Validation Tests

```bash
make test-validators
```

Test file: `tests/test_validators.py`

### Add Tests for Your Implementation

```python
import pytest
from backend.api.client import APIClient

@pytest.mark.asyncio
async def test_my_api_call():
    """Test my custom API call."""
    # Your test here
```

---

## Environment Variables

Configure behavior using environment variables:

```bash
# MCP Server configuration
export MCP_HOST=localhost
export MCP_PORT=3001

# API configuration
export API_BASE_URL=https://api.example.com

# Database (existing)
export DATABASE_URL=postgresql://user:pass@localhost/recipes
```

---

## Next Steps

1. **Implement API Clients**: Add specific API client implementations in `backend/api/` for external services
2. **Complete MCP Implementation**: Add tool handlers and resource handlers in `backend/mcp/server.py`
3. **Add FastAPI Routes**: Integrate with existing `api_server.py` using the patterns above
4. **Add Tests**: Implement tests in `tests/` following the provided examples
5. **Deploy**: Configure deployment using Docker Compose with MCP as separate service if needed

---

## Troubleshooting

### "Token expired and no refresh function provided"

Make sure you pass a `refresh_func` to `APIAuthManager`:

```python
auth_manager = APIAuthManager(refresh_func=my_refresh_func)
```

### MCP Server not starting

Check dependencies are installed:

```bash
pip install -r backend/requirements.txt
```

### Validation errors

Ensure all inputs match expected types and ranges. See `backend/utils/validators.py` for acceptable values.
