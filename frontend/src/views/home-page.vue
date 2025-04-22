<script setup>
import ContactsDetail from '@/components/contacts-detail.vue';
import ContactsTable from '@/components/contacts-table.vue';
</script>

<template>

  <div id="data-grid">
    <ContactsTable />
    <ContactsDetail/>
  </div>
</template>

<style lang="scss">
@use "../variables.scss" as *;
</style>