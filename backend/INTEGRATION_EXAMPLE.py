"""
Example integration of API and MCP modules into the FastAPI server.

This file demonstrates how to integrate the new backend/api/, backend/mcp/,
and backend/utils/ modules into your existing api_server.py.

Copy and adapt these patterns to your api_server.py as needed.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from backend.db import get_session, engine, Base
from backend.api.client import APIClient
from backend.api.auth import APIAuthManager
from backend.utils.validators import validate_budget, validate_dietary_preferences
from backend.utils.http import HTTPHelper
from backend.mcp.server import MCPServer


# Initialize FastAPI app (same as before)
app = FastAPI(title="Recipes API", version="1.0.0")

# Add CORS middleware (same as before)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP Server
mcp_server = MCPServer(host="localhost", port=3001)


# ============================================================================
# API CLIENT INTEGRATION EXAMPLE
# ============================================================================

async def get_api_client() -> APIClient:
    """Dependency to get configured API client."""
    async def refresh_token_func(user_id: str):
        # Implement your token refresh logic here
        # For example, call an external service or use refresh_access_token
        from backend.token_manager import refresh_access_token
        return refresh_access_token(user_id, lambda rt: (rt, None, 3600))
    
    auth_manager = APIAuthManager(refresh_func=refresh_token_func)
    return APIClient(
        base_url="https://api.example.com",  # Configure as needed
        auth_manager=auth_manager
    )


# ============================================================================
# MCP INTEGRATION ENDPOINTS
# ============================================================================

@app.get("/mcp/tools")
async def get_mcp_tools() -> Dict[str, Any]:
    """
    Get available MCP tools.
    
    Returns:
        Dictionary of tool names and schemas
    """
    return HTTPHelper.success_response(
        data=mcp_server.tools,
        message="Available MCP tools"
    )


@app.get("/mcp/resources")
async def get_mcp_resources() -> Dict[str, Any]:
    """
    Get available MCP resources.
    
    Returns:
        Dictionary of resource names and descriptions
    """
    return HTTPHelper.success_response(
        data=mcp_server.resources,
        message="Available MCP resources"
    )


@app.post("/mcp/call")
async def call_mcp_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call an MCP tool with parameters.
    
    Args:
        tool_name: Name of the tool to call
        params: Parameters for the tool
    
    Returns:
        Tool execution result
    """
    try:
        result = await mcp_server.handle_tool_call(tool_name, params)
        return HTTPHelper.success_response(data=result, message=f"Tool '{tool_name}' executed")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool execution failed: {str(e)}")


# ============================================================================
# EXAMPLE: MEAL PLAN WITH VALIDATION
# ============================================================================

@app.post("/meal-plans")
async def create_meal_plan(
    budget: float,
    servings: int,
    preferences: list,
    session: AsyncSession = Depends(get_session),
):
    """
    Create a meal plan with validated inputs.
    
    This example shows how to use the validation utilities.
    
    Args:
        budget: Weekly budget in dollars
        servings: Number of servings needed
        preferences: List of dietary preferences
        session: Database session
    
    Returns:
        Created meal plan details
    """
    # Validate inputs using utility functions
    try:
        validate_budget(budget)
        from backend.utils.validators import validate_servings
        validate_servings(servings)
        validate_dietary_preferences(preferences)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Generate meal plan (your logic here)
    meal_plan = {
        "id": "mp_123",
        "budget": budget,
        "servings": servings,
        "preferences": preferences,
        "recipes": [],
    }
    
    return HTTPHelper.success_response(data=meal_plan, message="Meal plan created")


# ============================================================================
# EXAMPLE: API CLIENT USAGE
# ============================================================================

@app.get("/external-recipes")
async def get_external_recipes(
    user_id: str,
    limit: int = 10,
    api_client: APIClient = Depends(get_api_client),
):
    """
    Fetch recipes from an external API using the API client.
    
    This example shows how to use the APIClient dependency.
    
    Args:
        user_id: User ID for authentication
        limit: Maximum number of recipes to return
        api_client: Injected API client
    
    Returns:
        List of recipes from external API
    """
    try:
        async with api_client:
            recipes = await api_client.get(
                endpoint="recipes",
                user_id=user_id,
                params={"limit": limit}
            )
        return HTTPHelper.success_response(data=recipes, message="External recipes fetched")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recipes: {str(e)}")


# ============================================================================
# STARTUP AND SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database and MCP server on startup."""
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize MCP server
    print("MCP Server tools registered:", len(mcp_server.tools))
    print("MCP Server resources registered:", len(mcp_server.resources))


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        Status of the API and MCP server
    """
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "mcp": "ready",
            "tools_registered": len(mcp_server.tools),
            "resources_registered": len(mcp_server.resources),
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
