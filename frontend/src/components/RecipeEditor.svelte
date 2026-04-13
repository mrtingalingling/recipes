<script>
  export let recipe = { title: '', ingredients: [], instructions: '' };
  function save() {
    // Save logic here
    $dispatch('save', recipe);
  }
</script>

<form on:submit|preventDefault={save}>
  <label>Title: <input type="text" bind:value={recipe.title} /></label>
  <label>Ingredients: <input type="text" bind:value={recipe.ingredients} placeholder="Comma separated" /></label>
  <label>Instructions: <textarea bind:value={recipe.instructions}></textarea></label>
  <button type="submit">Save</button>
</form>
