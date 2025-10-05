# Detailed User Stories & Functional Requirements with Tasks (Based on PRD & MVP Flow)

---

## **Epic 1: Budget Input & Personalization**

### User Stories

1. **As a user, I want to set a weekly budget so I can control how much I spend on groceries.**
2. **As a user, I want to specify the number of people I’m shopping for so the app scales recipes accordingly.**
3. **As a user, I want to add dietary preferences and restrictions so I only see relevant recipes.**
4. **As a user, I want to adjust my cooking time preference so I see recipes that fit my schedule.**

### Functional Requirements

* Input fields for budget amount, household size, dietary preferences.
* Slider for cooking time preference.
* Persistent storage of user preferences for reuse.

### Tasks

* T1: [Frontend] Build budget input screen UI.
* T2: [Frontend] Add fields for household size, dietary preferences, cooking time.
* T3: [Backend] Create user profile schema to store budget, preferences, household info.
* T4: [Backend] Save/Update user preferences in database.
* T5: [QA] Test validation for numeric inputs (budget, household size).
* T6: [QA] Test default values and edge cases (e.g., budget = $0).

---

## **Epic 2: Store Deals Integration**

### User Stories

1. **As a user, I want to see weekly store deals so I can plan meals around discounted items.**
2. **As a user, I want to view deals on a map so I can choose the closest or most affordable store.**
3. **As a user, I want to browse deals in a list so I can quickly compare prices across stores.**

### Functional Requirements

* Scraping engine for weekly circulars.
* Store database with geo-location.
* Map view and list view toggle.
* Linking deals to ingredient categories.

### Tasks

* T7: [Backend] Build scraping pipeline for weekly store ads using AI API that utilizes user's own token after a secure authentication and authorization during login. 
* T8: [Backend] Store normalized deal data in DB (store, product, price, validity dates).
* T9: [Frontend] Map view with pins for stores and deals popup.
* T10: [Frontend] List view of deals grouped by store.
* T11: [Backend] Create API endpoints for deals retrieval (by store, location, category).
* T12: [QA] Verify deal accuracy and store mapping.

---

## **Epic 3: Recipe Exploration**

### User Stories

1. **As a user, I want to explore new recipes I haven’t tried before so I can add variety to my meals.**
2. **As a user, I want to explore the healthiest recipes based on what’s on sale so I can eat well within my budget.**
3. **As a user, I want to explore the most popular/best recipes so I can try what others recommend.**
4. **As a user, I want to view recipes from external sources in-app so I don’t need to switch apps.**
5. **As a user, I want to modify or create recipes so I can personalize them to my needs.**

### Functional Requirements

* Recipe feed with three filter tabs: New, Healthiest, Popular.
* Recipe cards with title, thumbnail, and sale-linked ingredients.
* Mini iFrame or embedded view for external recipes.
* Recipe creation/editing module.

### Tasks

* T13: [Frontend] Create recipe exploration screen with tabs.
* T14: [Frontend] Build recipe card component.
* T15: [Frontend] Integrate iFrame viewer for external recipes.
* T16: [Frontend] Build recipe editing form (title, ingredients, instructions).
* T17: [Backend] Create recipe schema (user-generated + external reference).
* T18: [Backend] Link recipes with store deals.
* T19: [Backend] API for fetching recipe lists (filters: new, healthiest, popular).
* T20: [QA] Test filtering logic and external recipe rendering.

---

## **Epic 4: Meal Plan Generation**

### User Stories

1. **As a user, I want to generate a weekly meal plan so I don’t have to manually select all meals.**
2. **As a user, I want to see my plan in a calendar view so I can organize meals by day and meal type.**
3. **As a user, I want to swap or remove recipes from the plan so I can customize my schedule.**

### Functional Requirements

* Meal plan generator logic that respects budget, preferences, and deals.
* Calendar view layout.
* Drag-and-drop or long-press functionality to replace recipes.

### Tasks

* T21: [Backend] Develop meal plan generation algorithm.
* T22: [Backend] Endpoint to retrieve generated meal plan.
* T23: [Frontend] Calendar grid UI (Mon–Sun, breakfast/lunch/dinner slots).
* T24: [Frontend] Enable swapping/removing recipes.
* T25: [QA] Test budget alignment (plan should not exceed budget).
* T26: [QA] Test calendar interactions.

---

## **Epic 5: Shopping List Export**

### User Stories

1. **As a user, I want an automatically generated shopping list so I don’t miss ingredients.**
2. **As a user, I want my list grouped by store so I can shop efficiently.**
3. **As a user, I want to export my shopping list to PDF or Instacart so I can use it outside the app.**

### Functional Requirements

* Shopping list generator linked to meal plan.
* Grouping by recipe or by store.
* Export options (PDF, CSV, Instacart integration roadmap).

### Tasks

* T27: [Backend] Build shopping list generation logic.
* T28: [Frontend] Create shopping list screen with tabs (By Recipe | By Store).
* T29: [Frontend] Checkbox interactions for marking items.
* T30: [Backend] PDF/CSV export functionality.
* T31: [Backend] Future: API integration with Instacart.
* T32: [QA] Verify list accuracy against selected meal plan.

---

## **Epic 6: Profile & Preferences**

### User Stories

1. **As a user, I want to update my preferences anytime so the app reflects my changing needs.**
2. **As a user, I want to have a household account so I can plan meals for my family.**
3. **As a user, I want to save past meal plans so I can reuse them later.**

### Functional Requirements

* Profile management (budget, preferences, household members).
* Linked household accounts.
* Saved meal plan storage and retrieval.

### Tasks

* T33: [Frontend] Profile screen UI with editable fields.
* T34: [Backend] User schema with household link support.
* T35: [Backend] Storage of past meal plans.
* T36: [Frontend] Meal plan history view.
* T37: [QA] Test household linking and saved plan retrieval.

---

## **Cross-Epic Tasks**

* T38: [Security] Implement OAuth login (Google, Apple, Email).
* T39: [Data] Build initial database schema for users, recipes, deals, meal plans, shopping lists.
* T40: [Analytics] Track metrics: budget plans created, recipes explored, lists exported.
* T41: [Testing] End-to-end tests for the full flow: Budget → Deals → Recipes → Plan → List → Export.

---

✅ Each task now has a **unique Task ID** (T1–T41) for easier tracking, assignment, and sprint planning.
