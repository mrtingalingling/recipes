<script>
  export let profile = { username: '', budget: 0, preferences: '', household_id: null };
</script>

<form>
  <label>Username: <input type="text" bind:value={profile.username} /></label>
  <label>Budget: <input type="number" bind:value={profile.budget} /></label>
  <label>Preferences: <input type="text" bind:value={profile.preferences} /></label>
  <label>Household ID: <input type="number" bind:value={profile.household_id} /></label>
  <button type="submit">Save</button>
</form>
