<script setup lang="js">
import { ref } from 'vue';
import ContactsDetail from './contacts-detail.vue';
import { DxTabs, DxItem } from 'devextreme-vue/tabs';

const selectedTab = ref(0);

</script>

<template>
    <div v-if="selectedTab == 0">
        <ContactsDetail />
    </div>
    <div v-else-if="selectedTab == 1">
        <p>Profiles content goes here.</p>
    </div>
    <div v-else-if="selectedTab == 2">
        <p>Privacy content goes here.</p>
    </div>

    <DxTabs v-model:selected-index="selectedTab">
        <DxItem text="Contacts" />
        <DxItem text="Profiles" />
        <DxItem text="Privacy" />
    </DxTabs>
</template>