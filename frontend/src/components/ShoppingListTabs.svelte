<script>
  export let byRecipe = {};
  export let byStore = {};
  let activeTab = 'store';
</script>

<div>
  <button on:click={() => activeTab = 'store'}>By Store</button>
  <button on:click={() => activeTab = 'recipe'}>By Recipe</button>
  {#if activeTab === 'store'}
    <ul>
      {#each Object.entries(byStore) as [store, items]}
        <li><strong>{store}</strong>: {items.join(', ')}</li>
      {/each}
    </ul>
  {:else}
    <ul>
      {#each Object.entries(byRecipe) as [recipe, items]}
        <li><strong>{recipe}</strong>: {items.join(', ')}</li>
      {/each}
    </ul>
  {/if}
</div>
