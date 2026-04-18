<script>
  import BudgetInput from './components/BudgetInput.svelte';
  import HouseholdInput from './components/HouseholdInput.svelte';
  import DietaryPreferences from './components/DietaryPreferences.svelte';
  import CookingTimeSlider from './components/CookingTimeSlider.svelte';
</script>

<main>
  <h1>Recipe App</h1>
  <BudgetInput />
  <HouseholdInput />
  <DietaryPreferences />
  <CookingTimeSlider />
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
      'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans',
      'Helvetica Neue', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: #f5f5f5;
  }

  main {
    max-width: 1200px;
    margin: 0 auto;
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  h1 {
    color: #333;
    text-align: center;
    margin-top: 0;
  }
</style>
