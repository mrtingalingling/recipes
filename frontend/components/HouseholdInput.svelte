<script>
  export let householdSize = 1;
  let error = '';
  function validateSize(val) {
    if (val < 1) error = 'Household size must be at least 1';
    else error = '';
  }
</script>

<label>Household Size:
  <input type="number" bind:value={householdSize} on:input={() => validateSize(householdSize)} min="1" />
</label>
{#if error}
  <span class="error">{error}</span>
{/if}
