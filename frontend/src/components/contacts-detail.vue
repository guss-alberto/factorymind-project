<script setup lang="js">
import djangoStore from '@/utils/django-adapter';
import {
  DxDataGrid, DxEditing, DxForm,
  DxItem, DxPopup, DxFilterRow
} from 'devextreme-vue/data-grid';
import DxTabs from 'devextreme-vue/tabs';
import { ref, defineProps } from 'vue';

import { emailPattern, phonePattern, phoneNumberField } from '@/utils/validation-patterns';

let props = defineProps(["id"])

let selectedTab = ref(1)
/* eslint-disable */

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
    dataField: "sede", caption: "Nome sede", filterOperations: ['contains'],
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
    ]
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
      onKeyPress: phoneNumberField
    }
  },
  {
    dataField: "phone_ext", caption: "Telefono agg.", filterOperations: ['contains'], validationRules: [
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
      onKeyPress: phoneNumberField
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
    editorOptions: {
      onKeyPress: phoneNumberField
    }
  },
  {
    dataField: "country", caption: "Paese", filterOperations: ['contains'], lookup: {
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
    }
  },
  {
    dataField: "region", caption: "Provincia/stato", filterOperations: ['contains'],
    lookup: {
      dataSource: (options) => ({
        store: regions,
        filter: options.data ? ['country', '=', options.data.country] : null,
      }),
      valueExpr: "id",
      displayExpr: e => `${e.code} - ${e.name}`,
    },
    editorOptions: {
      searchEnabled: true,
      showClearButton: true,
    },
    async setCellValue(rowData, value) {
      rowData.region = value
      rowData.city = null
    }
  },

  {
    dataField: "city", caption: "Comune", filterOperations: ['contains'],
    lookup:
    {
      dataSource: (options) => ({
        store: cities,
        filter: options.data ? ['region', '=', options.data.region] : null,
      }),
      valueExpr: "id",
      displayExpr: "name",
    },
    editorOptions: {
      searchEnabled: true,
      showClearButton: true,
    },
  },
  {
    dataField: "address", caption: "Indirizzo", filterOperations: ['contains'],
    validationRules: [
      {
        type: 'required'
      }
    ]
  },
] 
</script>

<template>
  <div contacts v-if="selectedTab == 1">
    <DxDataGrid :data-source="aaa" :show-borders="true" :remote-operations="true" :columns="columns"
      @row-inserting="onRowInserting">
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
