<script>
  import DealsMapView from './DealsMapView.svelte';
  import DealsListView from './DealsListView.svelte';
  let deals = [];
  let view = 'map';

  // Dummy data for now
  deals = [
    { store_name: 'StoreA', product_name: 'Milk', price: 2.99, validity_start: '2025-10-01', validity_end: '2025-10-07', geo_location: '40.7128,-74.0060' },
    { store_name: 'StoreB', product_name: 'Bread', price: 1.99, validity_start: '2025-10-01', validity_end: '2025-10-07', geo_location: '34.0522,-118.2437' }
  ];
</script>

<div>
  <button on:click={() => view = 'map'}>Map View</button>
  <button on:click={() => view = 'list'}>List View</button>
  {#if view === 'map'}
    <DealsMapView {deals} />
  {:else}
    <DealsListView {deals} />
  {/if}
</div>
