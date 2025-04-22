<script setup lang="js">
import {
    DxDataGrid, DxFilterRow, DxEditing, DxPaging, DxPager, DxForm, DxPopup, DxItem
} from 'devextreme-vue/data-grid';
import djangoStore from '@/utils/django-adapter';


const columns = [
    { dataField: "first_name", caption: "Nome", filterOperations: ['contains'] },
    { dataField: "last_name", caption: "Cognome", filterOperations: ['contains'] },
    { dataField: "phone", caption: "Telefono", filterOperations: ['contains'] },
    { dataField: "mobile", caption: "Cellulare", filterOperations: ['contains'] },
    { dataField: "email", caption: "E-mail", filterOperations: ['contains'] },
]

const store = djangoStore("http://localhost:8000/api/contacts/register")
</script>


<template>
    <DxDataGrid :data-source="store" :show-borders="true" :remote-operations="true" key-expr="id" :columns="columns">
        <DxPaging :enabled="true" />
        <DxPager :visible="true" :show-page-size-selector="true" :allowed-page-sizes="[2, 5, 10, 20]" />
        <dx-filter-row :visible="true" />
        <DxEditing :allow-updating="true" :allow-adding="true" :allow-deleting="true" mode="popup">
            <DxPopup :show-title="true" title="Contatto" />
            <DxForm>
                <DxItem :col-count="2" :col-span="2" item-type="group">
                </DxItem>
            </DxForm>
        </DxEditing>
    </DxDataGrid>
</template>