<script setup lang="js">
import { ref } from 'vue';
import ContactsDEtail from './contacts-detail.vue';

const selectedTab = ref(0);

</script>

<template>
    <DxTabs v-model:selected-index="selectedTab">
        <DxItem text="Contacts" />
        <DxItem text="Profiles" />
        <DxItem text="Privacy" />
    </DxTabs>
       
    <div v-if="selectedTab === 0">
        <ContactsDetail />
    </div>
    <div v-else-if="selectedTab === 1">
        <p>Profiles content goes here.</p>
    </div>
    <div v-else-if="selectedTab === 2">
        <p>Privacy content goes here.</p>
    </div>
</template>