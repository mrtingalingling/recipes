<script>
  import RecipeCard from './RecipeCard.svelte';
  export let recipes = [];
</script>

<div class="feed">
  {#each recipes as recipe}
    <RecipeCard {recipe} />
  {/each}
</div>

<style>
.feed { display: flex; flex-wrap: wrap; }
</style>
