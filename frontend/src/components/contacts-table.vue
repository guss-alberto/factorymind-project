<script setup lang="js">
import {
    DxDataGrid, DxFilterRow, DxEditing, DxColumn, DxPaging, DxPager, DxForm, DxPopup, DxItem
} from 'devextreme-vue/data-grid';
import djangoStore from '@/utils/django-adapter';

const fields = [
    { name: "Nome sede", field: "sede", type: "string" },
    { name: "Ragione sociale", field: "name", type: "string" },
    { name: "Comune", field: "city", type: "string" },
    { name: "Telefono", field: "phone", type: "string" },
    { name: "E-mail", field: "email", type: "string" },
]

const store = djangoStore("http://localhost:8000/api/contacts/contacts")
</script>


<template>
    <DxDataGrid :data-source="store" :show-borders="true" :remote-operations="true" key-expr="id">
        <DxPaging :enabled="true" />
        <DxPager :visible="true" :show-page-size-selector="true" :allowed-page-sizes="[5, 7, 13, 20]" />
        <dx-filter-row :visible="true" />
        <DxEditing :allow-updating="true" :allow-adding="true" :allow-deleting="true" mode="popup">
            <DxPopup :show-title="true" title="Contatto" />
            <DxForm>
                <DxItem :col-count="2" :col-span="2" item-type="group">
                </DxItem>
            </DxForm>
        </DxEditing>

        <DxColumn v-for="f in fields" :key="f.field" :caption="f.name" :data-field="f.field" :data-type="f.type" />
    </DxDataGrid>
</template>