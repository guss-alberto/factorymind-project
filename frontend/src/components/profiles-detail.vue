<script setup>
import djangoStore from '@/utils/django-adapter';
import {
  DxDataGrid
} from 'devextreme-vue/data-grid';

import { defineProps, ref } from 'vue';

const props = defineProps(["id"]); 

const profiles = djangoStore("http://localhost:8000/api/contacts/profiles");
const suppliers = djangoStore("http://localhost:8000/api/contacts/suppliers", {excluded_id: props.id});
const divisions = djangoStore("http://localhost:8000/api/contacts/divisions", {excluded_supplier: props.id});
const signes = djangoStore("http://localhost:8000/api/contacts/signes", {excluded_supplier: props.id});

function onRowInserting(e) {
  e.data.client = props.id;
}

const gridConfig = ref({
  dataSource: {
    store: profiles,
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
      title: "Profili",
    },
    form: {
        items: [
          {
            itemType: "group",
            caption: "Fornitore",
            colCount: 2,
            colSpan: 2,
            items: ["supplier", "division"]
          },
          {
            itemType: "group",
            caption: "Profilo",
            colCount: 2,
            colSpan: 2,
            items: [ "sign", "corresponding_code"]
          } 
        ]
    }
  },
  columns: [

  {
      dataField: "supplier", caption: "Fornitore",
      allowEditing: true,
      lookup: {
        dataSource: suppliers,
        valueExpr: "id",
        displayExpr: e => `${e.last_name} ${e.first_name}`,
      },
      editorOptions: {
        showClearButton: true,
        searchEnabled: true,
      },
      async setCellValue(rowData, value) {
        rowData.supplier = value;
        rowData.division = null;
        rowData.sign = null;
      },
      validationRules: [{ type: 'required' }],
      visible: false,
    },
    {
      dataField: "supplier_display", caption: "Fornitore", allowFiltering: true, allowEditing: false, filterOperations: ['contains'],
    },
    {
      dataField: "division", caption: "Divisioni", allowFiltering: false, allowEditing: true,
      allowEditing: true,
      validationRules: [{ type: 'required' }],
      lookup: {
        dataSource: (options) => ({
          store: divisions,
          filter: options.data ? ['supplier', '=', options.data.supplier] : null,
          paginate: true
        }),
        valueExpr: "id",
        displayExpr: e => `${e.code} ${e.name}`,
      },
      async setCellValue(rowData, value, currentRowData) {
        rowData.division = value;
        if (!value) return;

        if (currentRowData.sign) {
          const selectedSign = await signes.byKey(currentRowData.sign);
          if (selectedSign.supplier !== currentRowData.supplier) {
            rowData.sign = null;  
          }
        }

        if (!currentRowData.division) {
          const selectedDivision = await divisions.byKey(value);
          rowData.supplier = selectedDivision.supplier;
        }
      },
      editorOptions: {
        showClearButton: true,
        searchEnabled: true,
      },
      visible: false,
    },
    {
      dataField: "division_display", caption: "Divisioni", allowFiltering: true, allowEditing: false, filterOperations: ['contains'],
    },
    {
      dataField: "sign", caption: "Sigla", filterOperations: ['contains'], allowFiltering: false, allowEditing: true,
      validationRules: [{ type: 'required' }],
      lookup: {
        dataSource: (options) => ({
          store: signes,
          filter: options.data ? ['supplier', '=', options.data.supplier] : null,
          paginate: true
        }),
        valueExpr: "id",
        displayExpr: e => `${e.code}`,
      },
      async setCellValue(rowData, value, currentRowData) {
        rowData.sign = value;
        if (!value) return;

        if (currentRowData.division) {
          const selectedDivision = await divisions.byKey(currentRowData.division);
          if (selectedDivision.supplier !== currentRowData.supplier) {
            rowData.division = null;
          }
        }

        if (!currentRowData.sign) {
          const selectedSign = await signes.byKey(value);
          rowData.supplier = selectedSign.supplier;
        }
      },
      editorOptions: { maxLength: 50 },
      visible: false,
    },
    {
      dataField: "sign_display", caption: "Sigla", allowFiltering: true, allowEditing: false, filterOperations: ['contains'],
    },
    {
      dataField: "corresponding_code", caption: "Cod. Corr.", filterOperations: ['contains'],
      allowFiltering: true, allowEditing: true,
      validationRules: [{ type: 'required' }],
      editorOptions: { maxLength: 50 }
    },
    
  ],
  
});
</script>

<template>
    <DxDataGrid v-bind="gridConfig" />
</template>