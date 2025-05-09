<script setup lang="js">
import { defineProps, ref } from 'vue';
import ContactsDetail from './contacts-detail.vue';
import  DivisionDetail  from './division-detail.vue';
import  ProfilesDetail  from './profiles-detail.vue';
import SubagenciesDetail from './subagencies-detail.vue'
import { DxTabs, DxItem } from 'devextreme-vue/tabs';

const selectedTab = ref(0);
const props = defineProps({
    id:  Number,    
    registry_type: String
})

const fornitore = props.registry_type == 'Fornitore' || props.registry_type == 'Cliente/Fornitore'
const cliente = props.registry_type == 'Cliente' || props.registry_type == 'Cliente/Fornitore'

</script>

<template>
    <div v-if="selectedTab == 0">
        <ContactsDetail :id="props.id"/>
    </div>
    <div v-else-if="selectedTab == 1" >
        <DivisionDetail :id="props.id" />
    </div>
    <div v-else-if="selectedTab == 2">
        <ProfilesDetail :id="props.id" />
    </div>
    <div v-else-if="selectedTab == 3">
        <SubagenciesDetail :id="props.id" />
        
    </div>

    <DxTabs v-model:selected-index="selectedTab">
        <DxItem text="Contatti" />
        <DxItem :visible= "cliente", text="Divisioni" />
        <DxItem :visible= "cliente", text="Profili"  />
        <DxItem :visible= "fornitore", text="Subagenzie" />
    </DxTabs>
</template>