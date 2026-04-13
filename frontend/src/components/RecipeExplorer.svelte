/**
 * Example Svelte component showing API integration
 * 
 * Demonstrates:
 * - Fetching data from the backend
 * - Loading/error states
 * - Using stores
 * - Calling MCP tools
 */

<script>
  import { onMount } from 'svelte';
  import {
    recipes,
    loadingStates,
    errorStates,
    currentMealPlan,
    userProfile,
    isLoading,
  } from '../stores/app.js';
  import { fetchRecipes, createMealPlan } from '../api/hooks.js';
  import { setLoading, setError, clearError } from '../stores/app.js';

  let filterType = 'new';
  let mealPlanCreated = false;

  onMount(async () => {
    await loadRecipes();
  });

  async function loadRecipes() {
    setLoading('recipes', true);
    clearError('recipes');
    try {
      const data = await fetchRecipes(filterType, 10);
      recipes.set(data);
    } catch (error) {
      setError('recipes', error.message);
      console.error('Error loading recipes:', error);
    } finally {
      setLoading('recipes', false);
    }
  }

  async function handleCreateMealPlan() {
    setLoading('mealPlan', true);
    clearError('mealPlan');
    try {
      const plan = await createMealPlan(
        $userProfile.budget,
        $userProfile.servings,
        $userProfile.preferences
      );
      currentMealPlan.set(plan);
      mealPlanCreated = true;
    } catch (error) {
      setError('mealPlan', error.message);
      console.error('Error creating meal plan:', error);
    } finally {
      setLoading('mealPlan', false);
    }
  }

  function changeFilter(type) {
    filterType = type;
    loadRecipes();
  }
</script>

<div class="recipes-container">
  <h2>Recipes</h2>

  <div class="filter-buttons">
    <button
      class:active={filterType === 'new'}
      disabled={$isLoading}
      on:click={() => changeFilter('new')}
    >
      New
    </button>
    <button
      class:active={filterType === 'healthiest'}
      disabled={$isLoading}
      on:click={() => changeFilter('healthiest')}
    >
      Healthiest
    </button>
    <button
      class:active={filterType === 'popular'}
      disabled={$isLoading}
      on:click={() => changeFilter('popular')}
    >
      Popular
    </button>
  </div>

  {#if $loadingStates.recipes}
    <div class="loading">Loading recipes...</div>
  {:else if $errorStates.recipes}
    <div class="error">
      <p>Failed to load recipes: {$errorStates.recipes}</p>
      <button on:click={loadRecipes}>Retry</button>
    </div>
  {:else if $recipes.length > 0}
    <div class="recipe-list">
      {#each $recipes as recipe (recipe.id)}
        <div class="recipe-card">
          <h3>{recipe.title}</h3>
          <p>{recipe.description}</p>
          {#if recipe.cooking_time}
            <p>⏱️ {recipe.cooking_time} mins</p>
          {/if}
        </div>
      {/each}
    </div>
  {:else}
    <p>No recipes found</p>
  {/if}

  <div class="meal-plan-section">
    <h3>Create Meal Plan</h3>
    <button
      on:click={handleCreateMealPlan}
      disabled={$isLoading || !$userProfile.budget}
    >
      {$loadingStates.mealPlan ? 'Creating...' : 'Generate Meal Plan'}
    </button>

    {#if $errorStates.mealPlan}
      <div class="error">Failed: {$errorStates.mealPlan}</div>
    {/if}

    {#if mealPlanCreated && $currentMealPlan.id}
      <div class="success">
        <p>✓ Meal plan created!</p>
        <p>Total: ${$currentMealPlan.totalPrice}</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .recipes-container {
    padding: 20px;
  }

  h2 {
    color: #333;
    border-bottom: 2px solid #007bff;
    padding-bottom: 10px;
  }

  .filter-buttons {
    display: flex;
    gap: 10px;
    margin: 20px 0;
  }

  button {
    padding: 8px 16px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
    cursor: pointer;
    transition: all 0.3s;
  }

  button:hover:not(:disabled) {
    background: #f0f0f0;
  }

  button.active {
    background: #007bff;
    color: white;
    border-color: #007bff;
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .loading,
  .error,
  .success {
    padding: 15px;
    border-radius: 4px;
    margin: 15px 0;
  }

  .loading {
    background: #e3f2fd;
    color: #1d64a1;
  }

  .error {
    background: #ffebee;
    color: #c62828;
  }

  .error button {
    margin-top: 10px;
    padding: 6px 12px;
    background: #c62828;
    color: white;
    border: none;
  }

  .success {
    background: #e8f5e9;
    color: #2e7d32;
  }

  .recipe-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin: 20px 0;
  }

  .recipe-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    background: #f9f9f9;
    transition: transform 0.2s;
  }

  .recipe-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .recipe-card h3 {
    margin-top: 0;
    color: #333;
  }

  .meal-plan-section {
    margin-top: 30px;
    padding: 20px;
    background: #f5f5f5;
    border-radius: 4px;
  }
</style>
