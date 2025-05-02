I
<script setup lang="js">
import djangoStore from '@/utils/django-adapter';
import {
  DxDataGrid, DxEditing,
  DxFilterRow,
  DxForm,
  DxItem, DxPopup,
  DxPager, DxPaging
} from 'devextreme-vue/data-grid';
import DxTabs from 'devextreme-vue/tabs';
import { defineProps, ref } from 'vue';

import { emailPattern, phoneNumberField, phonePattern } from '@/utils/validation-patterns';

let props = defineProps(["id"])

let selectedTab = ref(1)

const contacts = djangoStore("http://localhost:8000/api/contacts/contacts")
const aaa = {
  store: contacts,
  filter: ["register", "=", props.id],
}
function onRowInserting(e) {
  e.data.register = props.id
}


const sedi = djangoStore("http://localhost:8000/api/contacts/sedi")
const cities = djangoStore("http://localhost:8000/api/contacts/cities")
const countries = djangoStore("http://localhost:8000/api/contacts/countries")
const regions = djangoStore("http://localhost:8000/api/contacts/regions")


const columns = [
  {
    dataField: "sede", caption: "Nome sede", allowFiltering: false,
    validationRules: [
      {
        type: 'required'
      }
    ],
    lookup: {
      dataSource: sedi,
      valueExpr: "id",
      displayExpr: e => `${e.code} - ${e.name}`,
    },
    editorOptions: {
      searchEnabled: true,
    },
  },
  {
    dataField: "name", caption: "Ragione sociale", filterOperations: ['contains'],
    validationRules: [

      {
        type: 'required'
      }
    ], 
    editorOptions: {
      maxLength: 50,
    }
  },
  {
    dataField: "phone", caption: "Telefono", filterOperations: ['contains'], validationRules: [
      {
        type: 'pattern',
        pattern: phonePattern,
        message: 'Il cellulare deve contenere solo numeri (massimo 15 cifre) con un "+" opzionale all\'inizio'
      },
      {
        type: 'required'
      }
    ],
    editorOptions: {
      onKeyPress: phoneNumberField,
      maxLength: 20,
    }
  },
  {
    dataField: "phone_ext", caption: "Telefono agg.", filterOperations: ['contains'], validationRules: [
      {
        type: 'pattern',
        pattern: phonePattern,
        message: 'Il cellulare deve contenere solo numeri (massimo 15 cifre) con un "+" opzionale all\'inizio'
      },
    ],
    editorOptions: {
      onKeyPress: phoneNumberField,
      maxLength: 20,
    }
  },
  {
    dataField: "email", caption: "E-mail", filterOperations: ['contains'], validationRules: [
      {
        type: 'pattern',
        pattern: emailPattern,
        message: 'Inserisci un indirizzo email valido',
      },
      {
        type: 'required'
      }
    ],
  },
  {
    dataField: "country", caption: "Paese", allowFiltering: false,
    lookup: {
      dataSource: countries,
      valueExpr: "iso_code",
      displayExpr: e => `${e.iso_code} - ${e.name}`,
    },
    editorOptions: {
      showClearButton: true,
      searchEnabled: true,
    },
    async setCellValue(rowData, value) {
      rowData.country = value
      rowData.region = null
      rowData.city = null
    },
    validationRules: [
      {
        type: 'required'
      }
    ],
  },
  {
    dataField: "region", caption: "Provincia/stato", allowFiltering: false,
    lookup: {
      dataSource: (options) => ({
        store: regions,
        filter: options.data ? ['country', '=', options.data.country] : null,
        paginate: true
      }),
      valueExpr: "id",
      displayExpr: e => {
        if (e.code)
          return `${e.code} - ${e.name}`
        return e.name
      },
    },
    editorOptions: {
      searchEnabled: true,
      showClearButton: true,
    },
    async setCellValue(rowData, value) {
      rowData.region = value
      rowData.city = null
      if (!value) return

      if (!rowData.country) { // reverse cascading only if region is not selected
        const selectedRegion = await regions.byKey(value);
        rowData.country = selectedRegion.country;
      }
    },
    validationRules: [
      {
        type: 'required'
      }
    ],
  },

  {
    dataField: "city", caption: "Comune", allowFiltering: false,
    lookup:
    {
      dataSource: (options) => {
        let filter = null
        if (options.data?.region)
          filter = ['region', '=', options.data.region]
        else if (options.data?.country)
          filter = ['region__country', '=', options.data.country]
        return {
          store: cities,
          filter: filter,
          paginate: true
        }
      },
      valueExpr: "id",
      displayExpr: e => {
        if (e.postcode)
          return `${e.postcode} - ${e.name}`
        return e.name
      },
    },
    editorOptions: {
      searchEnabled: true,
      showClearButton: true,
    },
    validationRules: [
      {
        type: 'required'
      }
    ],
    async setCellValue(rowData, value) {
      rowData.city = value;
      if (!value) return

      if (!rowData.region) { // reverse cascading only if region is not selected
        const selectedCity = await cities.byKey(value);
        rowData.region = selectedCity.region;
      }
      if (!rowData.country) { // reverse cascading only if region is not selected
        const selectedRegion = await regions.byKey(rowData.region);
        rowData.country = selectedRegion.country;
      }
    },
  },
  {
    dataField: "address", caption: "Indirizzo", filterOperations: ['contains'],
    validationRules: [
      {
        type: 'required'
      }
    ],
    editorOptions: {
      maxLength: 50,
    }
  },
]
</script>

<template>
  <div contacts v-if="selectedTab == 1">
    <DxDataGrid :data-source="aaa" :show-borders="true" :remote-operations="true" :columns="columns"
      @row-inserting="onRowInserting">
      <DxPaging :enabled="true" />
      <DxPager :visible="true" :show-page-size-selector="true" :allowed-page-sizes="[2, 5, 10, 20]" />
      <dx-filter-row :visible="true" />
      <DxEditing :allow-updating="true" :allow-adding="true" :allow-deleting="true" mode="popup">
        <DxPopup :show-title="true" title="Contatto" />
        <DxForm>
          <DxItem :col-count="2" :col-span="2" item-type="group" caption="Informazioni">
            <DxItem data-field="sede" />
            <DxItem data-field="name" />
            <DxItem data-field="phone" />
            <DxItem data-field="phone_ext" />
            <DxItem data-field="email" />
          </DxItem>
          <DxItem :col-count="2" :col-span="2" item-type="group" caption="Indirizzo">
            <DxItem data-field="country" />
            <DxItem data-field="region" />
            <DxItem data-field="city" />
            <DxItem data-field="address" />
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
