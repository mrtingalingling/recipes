<script>
  export let deals = [];
</script>

<ul>
  {#each deals as deal}
    <li>
      <strong>{deal.store_name}</strong>: {deal.product_name} - ${deal.price} ({deal.validity_start} to {deal.validity_end})
    </li>
  {/each}
</ul>
