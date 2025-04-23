<script setup lang="js">
import {
    DxDataGrid, DxEditing, DxForm, DxPopup, DxItem
} from 'devextreme-vue/data-grid';
import DxTabs from 'devextreme-vue/tabs';
import djangoStore from '@/utils/django-adapter';
import { ref } from 'vue';

let selectedTab = ref(1)
/* eslint-disable */


const store = djangoStore("http://localhost:8000/api/contacts/contacts")
const cities = djangoStore("http://localhost:8000/api/contacts/cities")
const countries = djangoStore("http://localhost:8000/api/contacts/countries")
const regions = djangoStore("http://localhost:8000/api/contacts/regions")

async function onEditorPreparing(e) {
    if (e.parentType === 'dataRow' && e.dataField === 'city') {
        const isStateNotSet = e.row.data.region === undefined;

        e.editorOptions.disabled = isStateNotSet;
    }
};

const filteredCities = {
    store: cities,
    filter: null,
}

function getFilteredCities (){
    return filteredCities
}

const columns = [
    { dataField: "sede", caption: "Nome sede", filterOperations: ['contains'] },
    { dataField: "name", caption: "Ragione sociale", filterOperations: ['contains'] },
    {
        dataField: "country", caption: "Paese", filterOperations: ['contains'], lookup: {
            dataSource: countries,
            valueExpr: "iso_code",
            displayExpr: "name",
            editorOptions: {
                searchEnabled: true,
            }
        }
    },
    {
        dataField: "city", caption: "Comune", filterOperations: ['contains'], lookup:
        {
            dataSource: getFilteredCities,
            valueExpr: "id",
            displayExpr: "name",
            editorOptions: {
                searchEnabled: true,
            },
            calculateDisplayValue: (rowData) => {
                if (!rowData.city) return null;
                const city = cities.find(c => c.id === rowData.city);
                return city ? city.name : rowData.city;
            },
        }
    },
    {
        dataField: "region", caption: "Provincia/stato", filterOperations: ['contains'], visible: false, lookup: {
            dataSource: regions,
            valueExpr: "id",
            displayExpr: "name",
            editorOptions: {
                searchEnabled: true,
            }
        },
        setCellValue: (rowData, value) => {
            rowData.city = null;
            rowData.country = value.country
            filteredCities.filter = ["region", "=", value];
        }
    },
    { dataField: "phone", caption: "Telefono", filterOperations: ['contains'] },
    { dataField: "email", caption: "E-mail", filterOperations: ['contains'] },
]
</script>


<template>

    <div contacts v-if="selectedTab == 1">
        <DxDataGrid :data-source="store" :show-borders="true" :remote-operations="true" :columns="columns"
            @editor-preparing="onEditorPreparing">
            <DxEditing :allow-updating="true" :allow-adding="true" :allow-deleting="true" mode="popup">
                <DxPopup :show-title="true" title="Contatto" />
                <DxForm>
                    <DxItem :col-count="2" :col-span="2" item-type="group" name="address">
                        <DxItem data-field="name" />
                        <DxItem data-field="city" />
                        <DxItem data-field="country" />
                        <DxItem data-field="region" />
                    </DxItem>
                </DxForm>
            </DxEditing>
        </DxDataGrid>
    </div>
    <DxTabs v-model:selected-index="selectedTab">
        <DxItem text="Profiles" />
        <DxItem text="Contacts" />
        <DxItem text="Privacy" />
    </DxTabs>
</template>