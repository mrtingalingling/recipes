/**
 * Frontend API hooks for data fetching and mutations.
 * 
 * These hooks provide async data loading with loading/error/success states.
 */

import { api, APIError } from './client';

/**
 * Fetch recipes from the backend
 */
export async function fetchRecipes(filterType = 'new', limit = 10) {
  try {
    const response = await api.get('/recipes', {
      params: new URLSearchParams({ filter_type: filterType, limit }),
    });
    return response.data || [];
  } catch (error) {
    console.error('Failed to fetch recipes:', error);
    throw error;
  }
}

/**
 * Create a meal plan
 */
export async function createMealPlan(budget, servings, preferences) {
  try {
    const response = await api.post('/meal-plans', {
      budget,
      servings,
      preferences,
    });
    return response.data;
  } catch (error) {
    console.error('Failed to create meal plan:', error);
    throw error;
  }
}

/**
 * Get shopping list
 */
export async function getShoppingList(mealPlanId) {
  try {
    const response = await api.get(`/shopping-lists/${mealPlanId}`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch shopping list:', error);
    throw error;
  }
}

/**
 * Get store deals
 */
export async function getStoreDeals(location, products = []) {
  try {
    const params = new URLSearchParams({ location });
    if (products.length) {
      params.append('products', products.join(','));
    }
    const response = await api.get('/deals', { params });
    return response.data || [];
  } catch (error) {
    console.error('Failed to fetch store deals:', error);
    throw error;
  }
}

/**
 * Get user profile
 */
export async function getUserProfile() {
  try {
    const response = await api.get('/profile');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch user profile:', error);
    throw error;
  }
}

/**
 * Update user profile
 */
export async function updateUserProfile(profileData) {
  try {
    const response = await api.put('/profile', profileData);
    return response.data;
  } catch (error) {
    console.error('Failed to update user profile:', error);
    throw error;
  }
}

/**
 * Save recipe
 */
export async function saveRecipe(recipe) {
  try {
    const response = await api.post('/recipes', recipe);
    return response.data;
  } catch (error) {
    console.error('Failed to save recipe:', error);
    throw error;
  }
}

/**
 * MCP-specific hooks
 */

/**
 * Call MCP tool and get result
 */
export async function callMCPTool(toolName, params = {}) {
  try {
    const response = await api.post('/mcp/call', {
      tool_name: toolName,
      params,
    });
    return response.data;
  } catch (error) {
    console.error(`MCP tool call failed: ${toolName}`, error);
    throw error;
  }
}
