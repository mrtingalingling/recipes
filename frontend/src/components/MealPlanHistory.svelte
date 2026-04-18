<script>
  export let history = [];
</script>

<ul>
  {#each history as item}
    <li>{item[0]}: {item[1]}</li>
  {/each}
</ul>
