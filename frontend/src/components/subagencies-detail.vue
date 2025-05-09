<script setup>
import djangoStore from '@/utils/django-adapter';
import {
  DxDataGrid
} from 'devextreme-vue/data-grid';

import { defineProps, ref } from 'vue';

const props = defineProps(["id"]); 

const subagencies = djangoStore("http://localhost:8000/api/contacts/subagencies");
const clients = djangoStore("http://localhost:8000/api/contacts/clients");
const signes = djangoStore("http://localhost:8000/api/contacts/signes");
const deposits = djangoStore("http://localhost:8000/api/contacts/deposits");

function onRowInserting(e) {
  e.data.supplier = props.id;
}

const gridConfig = ref({
  dataSource: {
    store: subagencies,
    filter: ["supplier", "=", props.id],
  },
  remoteOperations: true,
  keyExpr: "id",
  paging: { enabled: true },
  pager: {
    visible: true,
    showPageSizeSelector: true,
    allowedPageSizes: [2, 5, 10, 20],
  },
  filterRow: { visible: true },
  onRowInserting,
  editing: {
    allowUpdating: true,
    allowAdding: true,
    allowDeleting: true,
    mode: "popup",
    popup: {
      showTitle: true,
      title: "SubAgenzie",
    },
    form: {
        items: [
          {
            itemType: "group",
            caption: "Cliente",
            colCount: 2,
            colSpan: 2,
            items: ["client"]
          },
          {
            itemType: "group",
            caption: "Profilo",
            colCount: 2,
            colSpan: 2,
            items: [ "sign", "corresponding_code"]
          },
          {
            itemType: "group",
            caption: "Destinazione Merce",
            colCount: 2,
            colSpan: 2,
            items: [ "deposit"]
          } 
        ]
    }
  },
  columns: [

  {
      dataField: "client", caption: "Cliente",
      allowEditing: true,
      lookup: {
        dataSource: clients,
        valueExpr: "id",
        displayExpr: e => `${e.last_name} ${e.first_name}`,
      },
      editorOptions: {
        showClearButton: true,
        searchEnabled: true,
      },
      validationRules: [{ type: 'required' }],
      visible: false,
    },
    {
      dataField: "client_display", caption: "Cliente", allowFiltering: true, allowEditing: false, filterOperations: ['contains'],
    },
    {
      dataField: "sign", caption: "Sigla", filterOperations: ['contains'],
      validationRules: [{ type: 'required' }],
      lookup: {
        dataSource: signes,
        valueExpr: "id",
        displayExpr: e => `${e.code}`,
      },
      editorOptions: { maxLength: 50 }
    },
    {
      dataField: "corresponding_code", caption: "Cod. Corr.", filterOperations: ['contains'],
      validationRules: [{ type: 'required' }],
      editorOptions: { maxLength: 50 }
    },
    {
      dataField: "deposit", caption: "Deposito", allowFiltering: false, allowEditing: true,
      validationRules: [{ type: 'required' }],
      lookup: {
        dataSource: deposits,
        valueExpr: "id",
        displayExpr: e => `${e.code} ${e.name}`,
      },
      editorOptions: {
        showClearButton: true,
        searchEnabled: true,
      },
    },
    
  ],
  
});
</script>

<template>
    <DxDataGrid v-bind="gridConfig" />
</template>