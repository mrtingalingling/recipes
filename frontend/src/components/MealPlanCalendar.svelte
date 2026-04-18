<script>
  export let mealPlan = [];
</script>

<table class="calendar">
  <thead>
    <tr>
      <th>Day</th>
      <th>Meal</th>
    </tr>
  </thead>
  <tbody>
    {#each mealPlan as meal, i}
      <tr>
        <td>{['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][i]}</td>
        <td>{meal.title}</td>
      </tr>
    {/each}
  </tbody>
</table>

<style>
.calendar { width: 100%; border-collapse: collapse; }
.calendar th, .calendar td { border: 1px solid #ccc; padding: 0.5em; }
</style>
