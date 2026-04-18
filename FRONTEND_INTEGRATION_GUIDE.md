"""
Frontend Integration Guide for Recipes App

This guide explains how the frontend communicates with the backend API 
and MCP services.
"""

## Frontend Architecture

```
frontend/src/
├── api/                      # API communication layer
│   ├── client.js            # Core API client (fetch wrapper)
│   ├── mcp.js               # MCP client for Claude integration
│   └── hooks.js             # Data fetching functions
├── stores/
│   └── app.js               # Svelte stores for state management
├── components/
│   ├── RecipeExplorer.svelte    # Example: Recipe API integration
│   └── MCPToolsPanel.svelte      # Example: MCP tool calling
└── utils/
    └── localStorage.js      # Existing local storage management
```

---

## Using the API Client

### Basic Setup

The frontend communicates with your FastAPI backend through a centralized API client:

```javascript
import { api } from './api/client.js';

// GET request
const recipes = await api.get('/recipes?filter_type=new');

// POST request
const mealPlan = await api.post('/meal-plans', {
  budget: 100,
  servings: 4,
  preferences: ['vegetarian']
});

// PUT request
const updated = await api.put('/profile', { budget: 150 });

// DELETE request
await api.delete('/recipes/123');
```

### Authentication

Tokens are automatically managed:

```javascript
import { api } from './api/client.js';

// Token is read from localStorage and added to headers automatically
// On login, store token:
localStorage.setItem('auth_token', responseToken);

// On logout:
localStorage.removeItem('auth_token');
```

---

## Using Data Fetching Hooks

Simplified API calls with built-in error handling:

```javascript
import { 
  fetchRecipes, 
  createMealPlan, 
  getShoppingList,
  getStoreDeals,
  getUserProfile,
  updateUserProfile
} from './api/hooks.js';

// Fetch recipes
const recipes = await fetchRecipes('healthiest', 10);

// Create meal plan
const plan = await createMealPlan(100, 4, ['vegetarian', 'gluten-free']);

// Get shopping list
const shopping = await getShoppingList(mealPlanId);

// Get store deals
const deals = await getStoreDeals('10001', ['chicken', 'broccoli']);
```

---

## Using Svelte Stores

Reactive global state management:

```javascript
import {
  recipes,
  currentMealPlan,
  userProfile,
  shoppingList,
  storeDeals,
  loadingStates,
  errorStates,
  isLoading
} from './stores/app.js';

// Subscribe to stores in components
<script>
  import { recipes, currentMealPlan } from './stores/app.js';

  <!-- Reactive updates whenever store changes -->
  <h2>Total Recipes: {$recipes.length}</h2>
  <p>Budget: ${$currentMealPlan.budget}</p>
</script>
```

### Managing Auth in Stores

```javascript
import { 
  auth,
  setAuthToken,
  clearAuth
} from './stores/app.js';

// On successful login
setAuthToken(token, userId);

// On logout
clearAuth();

// Check if authenticated
<script>
  import { auth } from './stores/app.js';
  
  {#if $auth.isAuthenticated}
    <p>Welcome, {$auth.userId}</p>
  {:else}
    <p>Please log in</p>
  {/if}
</script>
```

### Managing Loading/Error States

```javascript
import { 
  loadingStates, 
  errorStates,
  setLoading,
  setError,
  clearError
} from './stores/app.js';

async function loadData() {
  setLoading('recipes', true);
  clearError('recipes');
  try {
    const data = await fetchRecipes();
    recipes.set(data);
  } catch (error) {
    setError('recipes', error.message);
  } finally {
    setLoading('recipes', false);
  }
}

<!-- In component -->
{#if $loadingStates.recipes}
  <div>Loading...</div>
{:else if $errorStates.recipes}
  <div>Error: {$errorStates.recipes}</div>
{:else}
  <!-- Show data -->
{/if}
```

---

## Using the MCP Client

Call Claude-accessible tools from the frontend:

```javascript
import { mcp } from './api/mcp.js';

// Get available tools
const tools = await mcp.getTools();

// Get available resources
const resources = await mcp.getResources();

// Call a specific tool
const result = await mcp.callTool('create_meal_plan', {
  budget: 100,
  preferences: ['vegetarian'],
  servings: 4
});

// Get a resource
const recipes = await mcp.getResource('recipes://all');
```

---

## Example: Complete Recipe Integration

### Fetch and Display Recipes

```svelte
<script>
  import { onMount } from 'svelte';
  import { recipes, loadingStates, errorStates } from '../stores/app.js';
  import { fetchRecipes } from '../api/hooks.js';
  import { setLoading, setError } from '../stores/app.js';

  let filterType = 'new';

  onMount(async () => {
    setLoading('recipes', true);
    try {
      const data = await fetchRecipes(filterType);
      recipes.set(data);
    } catch (error) {
      setError('recipes', error.message);
    } finally {
      setLoading('recipes', false);
    }
  });

  async function changeFilter(type) {
    filterType = type;
    setLoading('recipes', true);
    try {
      const data = await fetchRecipes(filterType);
      recipes.set(data);
    } catch (error) {
      setError('recipes', error.message);
    } finally {
      setLoading('recipes', false);
    }
  }
</script>

<div>
  {#if $loadingStates.recipes}
    <p>Loading recipes...</p>
  {:else if $errorStates.recipes}
    <p>Error: {$errorStates.recipes}</p>
  {:else}
    <div class="recipe-grid">
      {#each $recipes as recipe (recipe.id)}
        <RecipeCard {recipe} />
      {/each}
    </div>
  {/if}
</div>
```

### Create Meal Plan

```svelte
<script>
  import { createMealPlan, getShoppingList } from '../api/hooks.js';
  import { userProfile, currentMealPlan, shoppingList } from '../stores/app.js';
  import { setLoading, setError } from '../stores/app.js';

  async function createPlan() {
    setLoading('mealPlan', true);
    try {
      const plan = await createMealPlan(
        $userProfile.budget,
        $userProfile.servings,
        $userProfile.preferences
      );
      currentMealPlan.set(plan);

      // Fetch shopping list
      const list = await getShoppingList(plan.id);
      shoppingList.set(list);
    } catch (error) {
      setError('mealPlan', error.message);
    } finally {
      setLoading('mealPlan', false);
    }
  }
</script>

<button on:click={createPlan}>Generate Meal Plan</button>
```

---

## Configuration

Set API endpoints via environment variables:

### `.env` or `.env.local`

```
VITE_API_URL=http://localhost:8000
VITE_MCP_URL=http://localhost:8000/mcp
```

### In `vite.config.js`

```javascript
export default {
  define: {
    'import.meta.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL || 'http://localhost:8000'),
    'import.meta.env.VITE_MCP_URL': JSON.stringify(process.env.VITE_MCP_URL || 'http://localhost:8000/mcp'),
  }
}
```

---

## Error Handling

All API calls should handle errors:

```javascript
import { APIError } from './api/client.js';

async function loadData() {
  try {
    const data = await api.get('/recipes');
  } catch (error) {
    if (error instanceof APIError) {
      if (error.status === 401) {
        // Handle unauthorized - redirect to login
      } else if (error.status === 400) {
        // Handle validation error
      } else {
        // Handle other errors
      }
    }
  }
}
```

---

## Data Flow

### Frontend → Backend API

```
User Action
    ↓
Svelte Component (RecipeExplorer.svelte)
    ↓
API Hook (fetchRecipes())
    ↓
API Client (api.get('/recipes'))
    ↓
FastAPI Backend (api_server.py)
    ↓
Database
    ↓
Response → Svelte Store → Component Update
```

### Frontend ↔ MCP Server

```
Frontend Component (MCPToolsPanel.svelte)
    ↓
MCP Hook (callMCPTool())
    ↓
MCP Client (mcp.callTool())
    ↓
Backend API (/mcp/call endpoint)
    ↓
MCP Server (backend/mcp/server.py)
    ↓
Tool Handler
    ↓
Result → Component Display
```

---

## Testing API Integration

```javascript
// test_api.js
import { api, APIError } from './api/client.js';

// Mock test
const mockResponse = { status: 'success', data: [{ id: 1, title: 'Recipe' }] };

// Or use actual API during development
try {
  const recipes = await api.get('/recipes');
  console.log('Recipes loaded:', recipes);
} catch (error) {
  console.error('Failed to load recipes:', error);
}
```

---

## Troubleshooting

### CORS Errors

If you get CORS errors, ensure backend has CORS middleware enabled (it does in api_server.py).

### Token Expiration

APIAuthManager on backend should handle token refresh. If frontend gets 401:

```javascript
if (error.status === 401) {
  clearAuth();
  // Redirect to login
}
```

### MCP Tools Not Available

Check that `/mcp/tools` endpoint exists and returns data:

```javascript
const tools = await api.get('/mcp/tools');
console.log('Available tools:', tools);
```

---

## Next Steps

1. **Update `App.svelte`** to import and use RecipeExplorer/MCPToolsPanel components
2. **Set environment variables** in `.env.local`
3. **Test API endpoints** using fetch or browser DevTools Network tab
4. **Add more components** following the example patterns
5. **Implement error boundary** component for better error handling
6. **Add loading skeletons** for better UX while fetching data
