<script setup>
import djangoStore from '@/utils/django-adapter';
import {
  DxDataGrid
} from 'devextreme-vue/data-grid';

import { defineProps, ref } from 'vue';

const props = defineProps(["id"]); 

const divisions = djangoStore("http://localhost:8000/api/contacts/divisions");

function onRowInserting(e) {
  e.data.client = props.id;
}

const gridConfig = ref({
  dataSource: {
    store: divisions,
    filter: ["client", "=", props.id],
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
          "code", "name", "supplier",
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
    
  ],
  
});
</script>

<template>
    <DxDataGrid v-bind="gridConfig" />
</template>