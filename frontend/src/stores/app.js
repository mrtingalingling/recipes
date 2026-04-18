/**
 * Svelte stores for managing application state
 * 
 * Includes:
 * - User authentication state
 * - Recipe/meal plan data
 * - UI state (loading, errors)
 * - Shopping list state
 */

import { writable, derived } from 'svelte/store';

/**
 * Authentication store
 */
export const auth = writable({
  token: localStorage.getItem('auth_token') || null,
  userId: localStorage.getItem('user_id') || null,
  isAuthenticated: !!localStorage.getItem('auth_token'),
});

/**
 * Update auth token
 */
export function setAuthToken(token, userId) {
  localStorage.setItem('auth_token', token);
  if (userId) {
    localStorage.setItem('user_id', userId);
  }
  auth.set({
    token,
    userId: userId || localStorage.getItem('user_id'),
    isAuthenticated: true,
  });
}

/**
 * Clear auth
 */
export function clearAuth() {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user_id');
  auth.set({
    token: null,
    userId: null,
    isAuthenticated: false,
  });
}

/**
 * User profile store
 */
export const userProfile = writable({
  budget: null,
  servings: 1,
  preferences: [],
  location: null,
  cookingTime: 30,
});

/**
 * Recipes store
 */
export const recipes = writable([]);

/**
 * Current meal plan
 */
export const currentMealPlan = writable({
  id: null,
  budget: null,
  servings: 1,
  preferences: [],
  recipes: [],
  totalPrice: 0,
});

/**
 * Shopping list store
 */
export const shoppingList = writable([]);

/**
 * Store deals store
 */
export const storeDeals = writable([]);

/**
 * Loading states for different operations
 */
export const loadingStates = writable({
  recipes: false,
  mealPlan: false,
  shoppingList: false,
  deals: false,
  profile: false,
});

/**
 * Error states
 */
export const errorStates = writable({
  recipes: null,
  mealPlan: null,
  shoppingList: null,
  deals: null,
  profile: null,
});

/**
 * Derived store: Total shopping list cost
 */
export const totalShoppingCost = derived(shoppingList, $shoppingList =>
  $shoppingList.reduce((sum, item) => sum + (item.price || 0), 0)
);

/**
 * Derived store: UI state (any loading or error)
 */
export const isLoading = derived(loadingStates, $states =>
  Object.values($states).some(v => v === true)
);

export const hasError = derived(errorStates, $states =>
  Object.values($states).some(v => v !== null)
);

/**
 * Helper to update loading state
 */
export function setLoading(key, isLoading) {
  loadingStates.update(states => ({ ...states, [key]: isLoading }));
}

/**
 * Helper to update error state
 */
export function setError(key, error) {
  errorStates.update(states => ({ ...states, [key]: error }));
}

/**
 * Helper to clear error state
 */
export function clearError(key) {
  errorStates.update(states => ({ ...states, [key]: null }));
}
