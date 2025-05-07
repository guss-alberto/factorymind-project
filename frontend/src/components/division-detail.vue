I
<script setup lang="js">
import djangoStore from '@/utils/django-adapter';
import {
  DxDataGrid
} from 'devextreme-vue/data-grid';

import { defineProps, ref } from 'vue';

const props = defineProps(["id"]); 

const divisions = djangoStore("http://localhost:8000/api/contacts/divisions");
const suppliers = djangoStore("http://localhost:8000/api/contacts/register");

function onRowInserting(e) {
  e.data.register = props.id;
}
console.log(props.id, 'Division Detail')

const gridConfig = ref({
  dataSource: {
    store: divisions,
    filter: ["register", "=", props.id],
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
      title: "Divisioni",
    },
    form: {
        items: [
    {
      dataField: "code",
      label: { text: "Codice" },
      editorType: "dxTextBox",
      validationRules: [{ type: "required" }]
    },
    {
      dataField: "name",
      label: { text: "Nome" },
      editorType: "dxTextBox",
      validationRules: [{ type: "required" }]
    },
    {
      dataField: "register",
      label: { text: "Fornitore" },
      editorType: "dxTextBox",
      validationRules: [{ type: "required" }]
    }
  ]
    }
  },
  columns: [
    {
      dataField: "code", caption: "Codice", allowFiltering: false, allowEditing: true,
      validationRules: [{ type: 'required' }],
      editorOptions: {
        showClearButton: true,
        searchEnabled: true,
      },
    },
    {
      dataField: "name", caption: "Nome", filterOperations: ['contains'],
      validationRules: [{ type: 'required' }],
      editorOptions: { maxLength: 50 }
    },
    {
      dataField: "suppliers", caption: "Fornitore",
      lookup: {
        dataSource: suppliers,
        valueExpr: "id",
        displayExpr: e => ` ${e.name}`
      },
      calculateDisplayValue: (rowData) => {
        return `${rowData.register}`;
      },
    },
  ],
  
});
</script>

<template>
  <DxDataGrid v-bind="gridConfig" />
</template>