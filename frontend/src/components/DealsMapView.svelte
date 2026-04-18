<script>
  export let deals = [];
</script>

<div id="map">
  {#each deals as deal}
    <div class="pin" style="left:{deal.geo_location.split(',')[1]}px;top:{deal.geo_location.split(',')[0]}px">
      <span>{deal.store_name}</span>
      <div class="popup">
        <strong>{deal.product_name}</strong><br>
        ${deal.price} <br>
        {deal.validity_start} - {deal.validity_end}
      </div>
    </div>
  {/each}
</div>

<style>
#map { position: relative; width: 100%; height: 400px; background: #eef; }
.pin { position: absolute; cursor: pointer; }
.popup { display: none; position: absolute; background: #fff; border: 1px solid #ccc; padding: 5px; }
.pin:hover .popup { display: block; }
</style>
