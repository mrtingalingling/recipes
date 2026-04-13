# Frontend, Backend, APIs, and MCP Integration Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         YOUR RECIPES APP                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    FRONTEND (Svelte)                        │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  Components and UI                                  │   │   │
│  │  │  - RecipeExplorer.svelte                            │   │   │
│  │  │  - MCPToolsPanel.svelte                             │   │   │
│  │  │  - Meal Plan, Shopping List, etc.                  │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                         ↓                                   │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  Svelte Stores (State Management)                   │   │   │
│  │  │  $recipes, $currentMealPlan, $shoppingList, etc     │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                         ↓                                   │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  API & Data Layer                                   │   │   │
│  │  │  - api/client.js (fetch wrapper + auth)             │   │   │
│  │  │  - api/hooks.js (recipe, meal plan, deals funcs)    │   │   │
│  │  │  - api/mcp.js (MCP tool calling)                    │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│           │                              │                         │
│           │ HTTP/JSON                   │ HTTP/JSON               │
│           ↓                              ↓                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                BACKEND (FastAPI)                           │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  REST API Routes (/api_server.py)                   │   │   │
│  │  │  GET  /recipes               ← fetchRecipes()       │   │   │
│  │  │  POST /meal-plans            ← createMealPlan()     │   │   │
│  │  │  GET  /shopping-lists/{id}   ← getShoppingList()    │   │   │
│  │  │  GET  /deals                 ← getStoreDeals()      │   │   │
│  │  │  PUT  /profile               ← updateUserProfile()  │   │   │
│  │  │  POST /mcp/call              ← callMCPTool()        │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                         ↓                                   │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  Business Logic & Utilities                          │   │   │
│  │  │  - backend/api/ (external API clients)               │   │   │
│  │  │  - backend/mcp/ (MCP tool implementations)           │   │   │
│  │  │  - backend/utils/ (validators, serializers)          │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │                         ↓                                   │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  Data Layer                                          │   │   │
│  │  │  - SQLAlchemy ORM (models.py)                        │   │   │
│  │  │  - PostgreSQL Database                              │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│           ↑                              ↑                         │
│           │ External API calls          │ Tool results            │
│           │                             ↓                         │
│  ┌────────┴─────────────────────────────────────────────────────┐   │
│  │            OPTIONAL: External Services & MCP Clients         │   │
│  │                                                               │   │
│  │  ┌─────────────────────┐  ┌──────────────────┐              │   │
│  │  │ External APIs       │  │ Claude / AI      │              │   │
│  │  │ - Grocery APIs      │  │ - MCP Protocol   │              │   │
│  │  │ - Nutrition API     │  │ - Claude Tools   │              │   │
│  │  │ - Deals Services    │  │                  │              │   │
│  │  └─────────────────────┘  └──────────────────┘              │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Interaction Flows

### 1️⃣ STANDARD API FLOW: Frontend → Backend API → Database

**User Action: "Show me healthiest recipes"**

```
┌─────────────────────────────────────────────────────────────────┐
│ Frontend (Svelte Component)                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  User clicks "Healthiest" button                                │
│          ↓                                                       │
│  Component calls: await fetchRecipes('healthiest', 10)          │
│          ↓                                                       │
│  hooks.js calls: api.get('/recipes', {                          │
│                    params: { filter_type: 'healthiest' }        │
│                  })                                              │
│          ↓                                                       │
│  client.js makes HTTP request:                                  │
│  GET http://localhost:8000/recipes?filter_type=healthiest      │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP GET (JSON)
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Backend (FastAPI)                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  api_server.py receives request:                                │
│  @app.get("/recipes")                                           │
│  async def get_recipes(filter_type: str = "new")                │
│          ↓                                                       │
│  Route queries database using SQLAlchemy ORM:                   │
│  SELECT * FROM recipes ORDER BY health_score DESC              │
│          ↓                                                       │
│  db.py executes query against PostgreSQL                        │
│          ↓                                                       │
│  models.py returns Recipe objects                               │
│          ↓                                                       │
│  utils/http.py serializes to JSON:                              │
│  {                                                              │
│    "status": "success",                                         │
│    "data": [                                                    │
│      { "id": 1, "title": "...", "health_score": 95 },          │
│      { "id": 2, "title": "...", "health_score": 92 }           │
│    ]                                                            │
│  }                                                              │
│          ↓                                                       │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP 200 (JSON)
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Frontend (Svelte Component)                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Response received from api.get()                               │
│          ↓                                                       │
│  recipes.set(response.data)  // Update Svelte store             │
│          ↓                                                       │
│  Component re-renders:                                          │
│  {#each $recipes as recipe}                                     │
│    <RecipeCard {recipe} />   // ← UI updates automatically      │
│  {/each}                                                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2️⃣ MUTATION FLOW: Frontend → Backend → Database → Frontend

**User Action: "Create a meal plan for $100 budget"**

```
┌─────────────────────────────────────────────────────────────────┐
│ Frontend Component (RecipeExplorer.svelte)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  User enters:                                                   │
│  - Budget: $100                                                 │
│  - Servings: 4                                                  │
│  - Preferences: ['vegetarian', 'gluten-free']                  │
│          ↓                                                       │
│  User clicks "Generate Meal Plan"                               │
│          ↓                                                       │
│  Component calls:                                               │
│  await createMealPlan(100, 4, ['vegetarian', 'gluten-free'])    │
│          ↓                                                       │
│  hooks.js calls: api.post('/meal-plans', {                      │
│                    budget: 100,                                 │
│                    servings: 4,                                 │
│                    preferences: [...]                           │
│                  })                                              │
│          ↓                                                       │
│  client.js makes HTTP request:                                  │
│  POST http://localhost:8000/meal-plans                          │
│  Content-Type: application/json                                 │
│  Authorization: Bearer {token}                                 │
│  Body: { "budget": 100, "servings": 4, ... }                   │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP POST (JSON)
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Backend (FastAPI)                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  api_server.py receives POST request:                           │
│  @app.post("/meal-plans")                                       │
│  async def create_meal_plan(budget, servings, preferences)      │
│          ↓                                                       │
│  VALIDATE inputs using utils/validators.py:                    │
│  ✓ validate_budget(budget)                                     │
│  ✓ validate_servings(servings)                                 │
│  ✓ validate_dietary_preferences(preferences)                   │
│          ↓                                                       │
│  BUSINESS LOGIC:                                                │
│  1. Query recipes matching preferences from DB                  │
│  2. Calculate recipes totaling to budget                        │
│  3. Create MealPlan record                                      │
│  4. Save to PostgreSQL                                          │
│          ↓                                                       │
│  db.py executes ORM query:                                      │
│  INSERT INTO meal_plans (user_id, budget, ...) VALUES (...)     │
│          ↓                                                       │
│  models.py returns MealPlan object                              │
│          ↓                                                       │
│  utils/http.py serializes to JSON:                              │
│  {                                                              │
│    "status": "success",                                         │
│    "message": "Meal plan created",                              │
│    "data": {                                                    │
│      "id": "mp_123abc",                                         │
│      "budget": 100,                                             │
│      "recipes": [ {...}, {...}, {...} ],                        │
│      "totalPrice": 98.50,                                       │
│      "created_at": "2026-04-13T10:30:00Z"                       │
│    }                                                            │
│  }                                                              │
│          ↓                                                       │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP 201 (JSON)
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Frontend Component (RecipeExplorer.svelte)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Response received: { status: "success", data: {...} }          │
│          ↓                                                       │
│  currentMealPlan.set(response.data)                             │
│  setLoading('mealPlan', false)                                  │
│  setError('mealPlan', null)                                     │
│          ↓                                                       │
│  Component re-renders with:                                     │
│  "✓ Meal plan created!"                                         │
│  "Total: $98.50"                                                │
│  List of selected recipes                                       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3️⃣ MCP TOOL CALL FLOW: Frontend → Backend MCP → Claude

**User Action: "Call an MCP tool to generate meal plan suggestions"**

```
┌─────────────────────────────────────────────────────────────────┐
│ Frontend Component (MCPToolsPanel.svelte)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  User selects "create_meal_plan" MCP tool                       │
│  User enters params:                                            │
│  - budget: 100                                                  │
│  - preferences: ['vegetarian']                                  │
│  - servings: 4                                                  │
│          ↓                                                       │
│  User clicks "Execute Tool"                                     │
│          ↓                                                       │
│  Component calls:                                               │
│  await mcp.callTool('create_meal_plan', {                       │
│    budget: 100,                                                 │
│    preferences: ['vegetarian'],                                 │
│    servings: 4                                                  │
│  })                                                              │
│          ↓                                                       │
│  api/mcp.js internally calls:                                   │
│  api.post('/mcp/call', {                                        │
│    tool_name: 'create_meal_plan',                               │
│    params: { budget: 100, ... }                                 │
│  })                                                              │
│          ↓                                                       │
│  client.js makes HTTP request:                                  │
│  POST http://localhost:8000/mcp/call                            │
│  Body: { "tool_name": "create_meal_plan", "params": {...} }     │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP POST
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Backend MCP Integration (api_server.py)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  FastAPI endpoint receives:                                     │
│  @app.post("/mcp/call")                                         │
│  async def call_mcp_tool(tool_name: str, params: dict)          │
│          ↓                                                       │
│  Instantiates MCPServer (from backend/mcp/server.py):          │
│  mcp_server.handle_tool_call(tool_name, params)                 │
│          ↓                                                       │
│  backend/mcp/server.py processes tool call:                    │
│  - Validates tool exists                                        │
│  - Maps tool name to implementation                             │
│  - Executes business logic (may query database)                 │
│  - Returns result dict                                          │
│          ↓                                                       │
│  Example implementation (to be implemented):                    │
│  async def handle_tool_call(tool_name, params):                │
│    if tool_name == "create_meal_plan":                         │
│      recipes = await db.query(Recipe).filter(...)              │
│      plan = calculate_meal_plan(recipes, params)               │
│      return { "status": "success", "data": plan }              │
│          ↓                                                       │
│  Returns JSON response:                                         │
│  {                                                              │
│    "status": "success",                                         │
│    "message": "Tool 'create_meal_plan' executed",               │
│    "data": {                                                    │
│      "recipes": [...],                                          │
│      "totalCost": 98.50,                                        │
│      "nutrition": {...}                                         │
│    }                                                            │
│  }                                                              │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP 200
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Frontend Component (MCPToolsPanel.svelte)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Response received from mcp.callTool()                          │
│          ↓                                                       │
│  Component displays result:                                     │
│  <div class="result">                                           │
│    <h5>Result</h5>                                              │
│    <pre>{ JSON stringify result }</pre>                         │
│  </div>                                                         │
│                                                                   │
│  Tool result can be used to:                                    │
│  - Create a meal plan automatically                             │
│  - Update UI with suggestions                                   │
│  - Pass data to other components                                │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ OPTIONAL: Claude is using your MCP tools                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Claude's MCP Client:                                           │
│  "User wants a vegetarian meal plan for 4 people under $100"    │
│          ↓                                                       │
│  Claude calls your tool:                                        │
│  mcp.callTool('create_meal_plan', {                             │
│    budget: 100,                                                 │
│    preferences: ['vegetarian'],                                 │
│    servings: 4                                                  │
│  })                                                              │
│          ↓                                                       │
│  Backend processes the same way (see above)                     │
│          ↓                                                       │
│  Claude receives result and:                                    │
│  - Provides personalized recommendations                        │
│  - Shows nutritional information                                │
│  - Explains substitutions                                       │
│  - Answers follow-up questions about the meal plan              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4️⃣ EXTERNAL API INTEGRATION FLOW

**Backend calling external services (grocery store APIs, nutrition APIs)**

```
┌─────────────────────────────────────────────────────────────────┐
│ Frontend Component                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  User asks: "Show me deals for these ingredients"               │
│          ↓                                                       │
│  Component calls: await getStoreDeals('10001', ['chicken'])     │
│          ↓                                                       │
│  HTTP POST /deals → Backend                                     │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Backend API Endpoint                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  @app.get("/deals")                                             │
│  async def get_store_deals(location, products):                 │
│          ↓                                                       │
│  Instantiates APIClient for external grocery service:           │
│  external_api = APIClient(                                      │
│    "https://groceryapi.example.com",                            │
│    auth_manager                                                 │
│  )                                                              │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
         ┌───────────────────┴───────────────────┐
         │                                       │
         ↓                                       ↓
┌──────────────────────┐            ┌──────────────────────┐
│ External Service 1   │            │ External Service 2   │
├──────────────────────┤            ├──────────────────────┤
│ Grocery Store API    │            │ Nutrition API        │
│ (Kroger, Safeway)    │            │ (USDA, MyFitnessPal) │
│                      │            │                      │
│ async with api:      │            │ async with api:      │
│   deals = await      │            │   nutrition = await  │
│   api.get(           │            │   api.get(           │
│     'products',      │            │     'nutrition',     │
│     params={...}     │            │     params={...}     │
│   )                  │            │   )                  │
│                      │            │                      │
│ Returns:             │            │ Returns:             │
│ [{name, store,       │            │ [{ingredient,        │
│   price, sale}]      │            │   calories, ...}]    │
└──────────────────────┘            └──────────────────────┘
         ↑                                       ↑
         │ HTTPs Request (with token)           │ HTTPs Request
         │ from APIClient                       │ from APIClient

┌─────────────────────────────────────────────────────────────────┐
│ Backend processes responses                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Combine results:                                               │
│  - Match deals with nutrition info                              │
│  - Sort by best value                                           │
│  - Filter by location                                           │
│  - Cache results in database                                    │
│          ↓                                                       │
│  Return to frontend as JSON:                                    │
│  {                                                              │
│    "status": "success",                                         │
│    "data": [{                                                   │
│      "product": "Chicken Breast",                               │
│      "store": "Kroger",                                         │
│      "price": 5.99,                                             │
│      "sale": true,                                              │
│      "nutrition": {                                             │
│        "calories": 165,                                         │
│        "protein": 31g                                           │
│      }                                                          │
│    }]                                                           │
│  }                                                              │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP 200 JSON
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Frontend displays deals                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  storeDeals.set(response.data)                                  │
│          ↓                                                       │
│  Component renders:                                             │
│  <DealsListView deals={$storeDeals} />                          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Complete Architecture Diagram with All Components

```
╔══════════════════════════════════════════════════════════════════════╗
║                        USER BROWSER (Frontend)                       ║
║  ┌──────────────────────────────────────────────────────────────┐   ║
║  │ Svelte Components (UI Layer)                                │   ║
║  │ ├─ App.svelte (root)                                        │   ║
║  │ ├─ RecipeExplorer.svelte (calls fetchRecipes)              │   ║
║  │ ├─ MCPToolsPanel.svelte (calls mcp.callTool)               │   ║
║  │ └─ Others (BudgetInput, ShoppingList, etc)                 │   ║
║  └──────────────────────────────────────────────────────────────┘   ║
║              │                                    │                  ║
║              ↓                                    ↓                  ║
║  ┌──────────────────────────────────────────────────────────────┐   ║
║  │ Svelte Stores (State Management)                            │   ║
║  │ ├─ $recipes (list of recipes)                               │   ║
║  │ ├─ $currentMealPlan                                         │   ║
║  │ ├─ $shoppingList                                            │   ║
║  │ ├─ $loadingStates, $errorStates                             │   ║
║  │ └─ $auth (user token, auth status)                          │   ║
║  └──────────────────────────────────────────────────────────────┘   ║
║              │                                    │                  ║
║              ↓                                    ↓                  ║
║  ┌──────────────────────────────────────────────────────────────┐   ║
║  │ API Layer (Communication)                                   │   ║
║  │ ├─ api/client.js (fetch wrapper + token auth)              │   ║
║  │ │  ├─ .get('/recipes') → GET request                       │   ║
║  │ │  ├─ .post('/meal-plans', data) → POST request            │   ║
║  │ │  └─ Token auto-injection from localStorage               │   ║
║  │ │                                                           │   ║
║  │ ├─ api/hooks.js (convenience functions)                    │   ║
║  │ │  ├─ fetchRecipes(filter, limit)                          │   ║
║  │ │  ├─ createMealPlan(budget, servings, prefs)              │   ║
║  │ │  ├─ getShoppingList(id)                                  │   ║
║  │ │  ├─ getStoreDeals(location)                              │   ║
║  │ │  └─ callMCPTool(toolName, params)                        │   ║
║  │ │                                                           │   ║
║  │ └─ api/mcp.js (MCP client)                                 │   ║
║  │    ├─ .callTool(toolName, params)                          │   ║
║  │    ├─ .getTools()                                          │   ║
║  │    └─ .getResources()                                      │   ║
║  └──────────────────────────────────────────────────────────────┘   ║
╚════════════════════════════════════════~~~~~~~~~~~~~~~~════════════════╝
                              │
                ┌─────────────┴──────────────┐
                │ HTTP/JSON over CORS        │
                ↓                            ↓
╔═══════════════════════════════════════════════════════════════════════╗
║                     SERVER (Backend - FastAPI)                        ║
║  ┌─────────────────────────────────────────────────────────────────┐  ║
║  │ API Routes (api_server.py)                                      │  ║
║  │                                                                 │  ║
║  │ GET  /recipes                → get_recipes()                   │  ║
║  │ POST /meal-plans             → create_meal_plan()              │  ║
║  │ GET  /shopping-lists/{id}    → get_shopping_list()             │  ║
║  │ GET  /deals                  → get_store_deals()               │  ║
║  │ GET  /profile                → get_user_profile()              │  ║
║  │ PUT  /profile                → update_user_profile()           │  ║
║  │ POST /mcp/call               → call_mcp_tool()                 │  ║
║  │ GET  /mcp/tools              → get_mcp_tools()                 │  ║
║  │ GET  /mcp/resources          → get_mcp_resources()             │  ║
║  │                                                                 │  ║
║  │ Middleware: CORS, Auth, Error Handling                         │  ║
║  └─────────────────────────────────────────────────────────────────┘  ║
║       │                          │                      │              ║
║       ↓                          ↓                      ↓              ║
║  ┌──────────────────────────────────────────────────────────────────┐  ║
║  │ Business Logic Layer                                            │  ║
║  │                                                                 │  ║
║  │ ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐   │  ║
║  │ │ API Clients     │  │ MCP Server       │  │ Utilities    │   │  ║
║  │ │ (backend/api/)  │  │ (backend/mcp/)   │  │ (backend/    │   │  ║
║  │ │                 │  │                  │  │  utils/)     │   │  ║
║  │ ├─APIClient       │  ├─MCPServer       │  ├─HTTPHelper   │   │  ║
║  │ │ .get()          │  │ .tools {}        │  ├─validators   │   │  ║
║  │ │ .post()         │  │ .resources {}    │  └─serializers  │   │  ║
║  │ │ .put()          │  │ .handle_tool_    │                 │   │  ║
║  │ │ .delete()       │  │  call()          │                 │   │  ║
║  │ │                 │  │ .handle_resource │                 │   │  ║
║  │ ├─APIAuthManager  │  │ _request()       │                 │   │  ║
║  │ │ .get_valid_     │  │                  │                 │   │  ║
║  │ │  token()        │  │ Tools:           │                 │   │  ║
║  │ │ Auto-refresh    │  │ - get_recipes    │                 │   │  ║
║  │ └─────────────────┘  │ - create_meal    │                 │   │  ║
║  │                      │   _plan          │                 │   │  ║
║  │                      │ - get_shopping   │                 │   │  ║
║  │                      │   _list          │                 │   │  ║
║  │                      │ - ... (add more) │                 │   │  ║
║  │                      └──────────────────┘                 │   │  ║
║  └──────────────────────────────────────────────────────────────────┘  ║
║       │                                                               │  ║
║       ↓                                                               ↓  ║
║  ┌──────────────────────────────────────────────────────────────────┐  ║
║  │ Data Layer                                                       │  ║
║  │                                                                 │  ║
║  │ ┌────────────────────────────────────────────────────────────┐ │  ║
║  │ │ SQLAlchemy ORM (models.py)                                 │ │  ║
║  │ │ ├─ Recipe model                                            │ │  ║
║  │ │ ├─ MealPlan model                                          │ │  ║
║  │ │ ├─ ShoppingList model                                      │ │  ║
║  │ │ ├─ User/Profile model                                      │ │  ║
║  │ │ └─ ...other models                                         │ │  ║
║  │ └────────────────────────────────────────────────────────────┘ │  ║
║  │       │                                                         │  ║
║  │       ↓                                                         │  ║
║  │ ┌────────────────────────────────────────────────────────────┐ │  ║
║  │ │ PostgreSQL Database (docker postgres service)              │ │  ║
║  │ │ ├─ recipes (table)                                         │ │  ║
║  │ │ ├─ meal_plans (table)                                      │ │  ║
║  │ │ ├─ shopping_lists (table)                                  │ │  ║
║  │ │ ├─ store_deals (table)                                     │ │  ║
║  │ │ └─ user_profiles (table)                                   │ │  ║
║  │ └────────────────────────────────────────────────────────────┘ │  ║
║  └──────────────────────────────────────────────────────────────────┘  ║
║       │                                                               │  ║
║       └────────────────────────────────────────────────────────────┬─┘  ║
║            Uses for caching & reference data                       │    ║
╚════════════════════════════════════════════════════════════════════════╝
             │                                                    │
             │ Makes HTTP calls to external services             │
             │ (if needed - optional)                            │
             │                                                    │
             ↓                                                    ↓
╔════════════════════════════════════╦════════════════════════════════╗
║    EXTERNAL SERVICES (Optional)    ║    CLAUDE / MCP CLIENTS        ║
║                                    ║                                ║
║ • Grocery Store APIs               ║ • Claude Desktop/Dashboard     ║
║   (Kroger, Safeway, etc)           ║ • Custom AI Agents             ║
║                                    ║ • Other MCP-enabled tools      ║
║ • Nutrition APIs                   ║                                ║
║   (USDA, MyFitnessPal)             ║ Uses same MCP endpoints:       ║
║                                    ║ • GET /mcp/tools               ║
║ • Recipe databases                 ║ • GET /mcp/resources           ║
║   (Spoonacular, Edamam)            ║ • POST /mcp/call               ║
║                                    ║                                ║
║ Used by backend/api/ module        ║ Accesses your recipes app      ║
║ via APIClient for data             ║ as a tool/resource provider    ║
║                                    ║                                ║
╚════════════════════════════════════╩════════════════════════════════╝
```

---

## Request/Response Cycle Summary

### Key Principles

1. **Frontend**: User interactions → API calls → Store updates → UI re-renders
2. **Backend**: HTTP request → Validate input → Business logic → Query database → Return JSON
3. **MCP**: Frontend or Claude → `/mcp/call` endpoint → MCPServer tool handler → Result
4. **External APIs**: Backend client → External service → Cache/use result

### Authentication Flow

```
Frontend:
  1. login() → Send credentials → Receive token
  2. localStorage.setItem('auth_token', token)
  3. All subsequent requests have Authorization: Bearer {token}

Backend:
  1. Validates token in each request
  2. token_manager.py manages token refresh
  3. APIAuthManager auto-refreshes expired tokens
```

### Error Handling

```
Frontend Error Handling:
  api.get() → APIError thrown
  ↓
  catch (error) {
    if (error.status === 401) → Redirect to login
    if (error.status === 400) → Show validation error
    if (error.status === 500) → Show server error
    setError('key', error.message) → Update store
  }

Backend Error Handling:
  validate() → ValueError → HTTPException(400)
  query() → SQLError → HTTPException(500)
  external_api() → Timeout → HTTPException(503)
  
  All return: {
    "status": "error",
    "status_code": 400,
    "message": "Human readable error"
  }
```

---

## Data Security

1. **CORS**: Backend allows frontend to make requests (configured in api_server.py)
2. **Authentication**: Tokens stored in localStorage, sent in Authorization header
3. **Validation**: All inputs validated on backend before database operations
4. **External APIs**: APIClient handles secure token refresh for external services

---

## Development Workflow

```
You code in Frontend:
  Component.svelte → import { api } from './api/client'
  → Call api.get('/recipes')
  → Backend must have @app.get("/recipes") endpoint

You code in Backend:
  api_server.py → Add @app.post("/new-endpoint")
  → Can be called from Frontend via api.post('/new-endpoint', data)

You add MCP Tool:
  backend/mcp/server.py → Add to self.tools
  → Frontend can call via mcp.callTool('tool_name', params)
  → Claude can call the same tool if you enable MCP

You need external data:
  backend/api/client.py → Instantiate APIClient
  → Make authenticated calls to external services
  → Cache in database
  → Frontend fetches from your API, not external service
```

---

## Testing the Integration

```javascript
// In browser console while app is running:

// 1. Test Frontend → Backend
const response = await fetch('http://localhost:8000/recipes');
const data = await response.json();
console.log(data); // Should show recipes

// 2. Test Frontend API client
import { api } from './api/client.js';
const recipes = await api.get('/recipes');
console.log(recipes);

// 3. Test MCP tools
import { mcp } from './api/mcp.js';
const tools = await mcp.getTools();
console.log(tools);

// 4. Check stores
import { recipes } from './stores/app.js';
recipes.subscribe(r => console.log('Recipes:', r));
```

This covers the complete flow!
