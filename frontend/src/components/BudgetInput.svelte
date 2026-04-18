<script>
  export let value = 0;
  let error = '';
  function validateBudget(val) {
    if (val < 0) error = 'Budget must be positive';
    else error = '';
  }
</script>

<label>Weekly Budget ($):
  <input type="number" bind:value on:input={() => validateBudget(value)} min="0" />
</label>
{#if error}
  <span class="error">{error}</span>
{/if}
