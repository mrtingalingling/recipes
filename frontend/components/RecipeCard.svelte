<script>
  export let recipe;
</script>

<div class="card">
  <img src={recipe.thumbnail} alt={recipe.title} />
  <h2>{recipe.title}</h2>
  <ul>
    {#each recipe.ingredients as ingredient}
      <li>{ingredient.name} {ingredient.onSale ? '(On Sale)' : ''}</li>
    {/each}
  </ul>
</div>

<style>
.card { border: 1px solid #ccc; padding: 1em; margin: 1em; }
img { width: 100px; height: 100px; object-fit: cover; }
</style>
