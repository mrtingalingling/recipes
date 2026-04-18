<script>
  export let activeTab = 'new';
  let tabs = ['new', 'healthiest', 'popular'];
  function selectTab(tab) {
    activeTab = tab;
    $dispatch('tabChange', tab);
  }
</script>

<div class="tabs">
  {#each tabs as tab}
    <button class:active={activeTab === tab} on:click={() => selectTab(tab)}>{tab.charAt(0).toUpperCase() + tab.slice(1)}</button>
  {/each}
</div>

<style>
.tabs button.active { font-weight: bold; }
</style>
