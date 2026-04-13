/**
 * Quick Start: Frontend API Integration
 * 
 * This file shows the fastest way to integrate API calls in your components
 */

import { onMount } from 'svelte';
import { api } from './api/client.js';
import { mcp } from './api/mcp.js';
import { recipes, currentMealPlan, setLoading, setError } from './stores/app.js';

/**
 * QUICK START: 1. Fetch recipes
 */
export async function quickFetchRecipes() {
  setLoading('recipes', true);
  try {
    const data = await api.get('/recipes?filter_type=new&limit=10');
    recipes.set(data.data);
  } catch (error) {
    setError('recipes', error.message);
  } finally {
    setLoading('recipes', false);
  }
}

/**
 * QUICK START: 2. Create meal plan
 */
export async function quickCreateMealPlan(budget, servings, preferences) {
  setLoading('mealPlan', true);
  try {
    const data = await api.post('/meal-plans', { budget, servings, preferences });
    currentMealPlan.set(data.data);
    return data.data;
  } catch (error) {
    setError('mealPlan', error.message);
    throw error;
  } finally {
    setLoading('mealPlan', false);
  }
}

/**
 * QUICK START: 3. Call MCP tool directly
 */
export async function quickCallMCPTool(toolName, params) {
  try {
    const result = await mcp.callTool(toolName, params);
    return result.data;
  } catch (error) {
    console.error(`Tool call failed: ${toolName}`, error);
    throw error;
  }
}

/**
 * Minimal Component Example
 */
// <script>
//   import { quickFetchRecipes, quickCreateMealPlan } from './quickstart.js';
//   import { recipes, loadingStates } from './stores/app.js';
//   import { onMount } from 'svelte';
//
//   onMount(quickFetchRecipes);
//
//   let budget = 100;
//
//   async function handleCreatePlan() {
//     await quickCreateMealPlan(budget, 4, ['vegetarian']);
//   }
// </script>
//
// <div>
//   {#if $loadingStates.recipes}
//     Loading recipes...
//   {:else}
//     <h2>Recipes ({$recipes.length})</h2>
//     <button on:click={handleCreatePlan}>Create Meal Plan</button>
//   {/if}
// </div>

/**
 * Step-by-step setup:
 * 
 * 1. Add to your Svelte component:
 *    import { api } from './api/client.js';
 *    import { recipes } from './stores/app.js';
 *
 * 2. In your component script:
 *    onMount(async () => {
 *      const data = await api.get('/recipes');
 *      recipes.set(data.data);
 *    });
 *
 * 3. In your markup:
 *    {#each $recipes as recipe}
 *      <div>{recipe.title}</div>
 *    {/each}
 *
 * That's it! The stores handle reactivity and the API client handles HTTP.
 */
