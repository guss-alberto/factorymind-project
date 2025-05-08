<script setup lang="js">
import { defineProps, ref } from 'vue';
import ContactsDetail from './contacts-detail.vue';
import  DivisionDetail  from './division-detail.vue';
import  ProfilesDetail  from './profiles-detail.vue';
import { DxTabs, DxItem } from 'devextreme-vue/tabs';

const selectedTab = ref(0);
const props = defineProps({
    id:  Number,
    registry_type: String
})

</script>

<template>
    <div v-if="selectedTab == 0">
        <ContactsDetail :id="props.id"/>
    </div>
    <div v-else-if="selectedTab == 1 && (props.registry_type == 'Cliente' || props.registry_type == 'Cliente/Fornitore')">
        <ProfilesDetail :id="props.id" />
    </div>
    <div v-else-if="selectedTab == 2">
        <DivisionDetail :id="props.id" />
        
    </div>

    <DxTabs v-model:selected-index="selectedTab">
        <DxItem text="Contatti" />
        <DxItem 
            text="Profili"  
        />
        <DxItem text="Divisioni" />
        <DxItem text="Subagenzie" />
    </DxTabs>
</template>