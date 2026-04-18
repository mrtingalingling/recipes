<script>
  export let cookingTime = 30;
</script>

<label>Cooking Time (minutes):
  <input type="range" min="10" max="120" step="5" bind:value={cookingTime} />
  <span>{cookingTime} min</span>
</label>
