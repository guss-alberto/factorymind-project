<script setup>
import registerTable from '@/components/register-table.vue';
</script>


<template>
  <div id="root">
    <div :class="cssClasses">
      <registerTable/>
    </div>
  </div>
</template>

<style lang="scss">
html,
body {
  margin: 0px;
  min-height: 100%;
  height: 100%;
}

#root {
  height: 100%;
}

* {
  box-sizing: border-box;
}

.app {
  display: flex;
  height: 100%;
  width: 100%;
  min-width: 320px;
}
</style>
