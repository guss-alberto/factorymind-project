<script setup>
import ContactsDetail from '@/components/contacts-detail.vue';
import RegisterTable from '@/components/register-table.vue';
</script>

<template>

  <div id="data-grid">
    <RegisterTable />
    <ContactsDetail/>
  </div>
</template>

<style lang="scss">
@use "../variables.scss" as *;
</style>