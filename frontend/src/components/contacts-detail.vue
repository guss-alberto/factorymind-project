I
<script setup lang="js">
import djangoStore from '@/utils/django-adapter';
import {
  DxDataGrid
} from 'devextreme-vue/data-grid';

import { defineProps, ref } from 'vue';
import { emailPattern, phoneNumberField, phonePattern } from '@/utils/validation-patterns';

const props = defineProps(["id"]);

const contacts = djangoStore("http://localhost:8000/api/contacts/contacts");
const branches = djangoStore("http://localhost:8000/api/contacts/branches");
const cities = djangoStore("http://localhost:8000/api/contacts/cities");
const countries = djangoStore("http://localhost:8000/api/contacts/countries");
const regions = djangoStore("http://localhost:8000/api/contacts/regions");

// Function to automatically assign the register ID when adding a row
function onRowInserting(e) {
  e.data.register = props.id;
}
console.log(props.id)


const gridConfig = ref({
  dataSource: {
    store: contacts,
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
      title: "Contatto",
    },
    form: {
      items: [
        {
          itemType: "group",
          caption: "Informazioni",
          colCount: 2,
          colSpan: 2,
          items: ["branch", "name", "phone", "phone_ext", "email"],
        },
        {
          itemType: "group",
          caption: "Indirizzo",
          colCount: 2,
          colSpan: 2,
          items: ["country", "region", "city", "address"],
        },
      ]
    }
  },

  onEditorPreparing(e) {
    if (e.dataField === 'region') {
      e.editorOptions.disabled = e.row?.data?.disable_region;
      if (e.editorOptions.disabled) {
        e.editorOptions.value = null;
        e.validationRules = e.validationRules.filter(rule => rule.type !== 'required');
      }
    }
  },

  onSaving(e) {
    e.changes.forEach(change => {
      const isRegionDisabled = change.data.disable_region;
      
      if (isRegionDisabled && !('region' in change.data)) {
        change.data.region = null;
      }
    });
  },

  columns: [
    {
      dataField: "branch", caption: "Nome sede", allowFiltering: false, allowEditing: true,
      validationRules: [{ type: 'required' }],
      lookup: {
        dataSource: branches,
        valueExpr: "id",
        displayExpr: e => `${e.code} - ${e.name}`,
      },
      editorOptions: {
        showClearButton: true,
        searchEnabled: true,
      },
      visible: false,
    },
    {
      dataField: "branch_display", caption: "Nome sede", allowFiltering: true, allowEditing: false, filterOperations: ['contains'],
    },
    {
      dataField: "name", caption: "Ragione sociale", filterOperations: ['contains'],
      validationRules: [{ type: 'required' }],
      editorOptions: { maxLength: 50 }
    },
    {
      dataField: "phone", caption: "Telefono", filterOperations: ['contains'],
      validationRules: [
        {
          type: 'pattern',
          pattern: phonePattern,
          message: 'Il cellulare deve contenere solo numeri (massimo 15 cifre) con un "+" opzionale all\'inizio'
        },
        { type: 'required' }
      ],
      editorOptions: {
        onKeyPress: phoneNumberField,
        maxLength: 20,
      }
    },
    {
      dataField: "phone_ext", caption: "Telefono agg.", filterOperations: ['contains'],
      validationRules: [
        {
          type: 'pattern',
          pattern: phonePattern,
          message: 'Il cellulare deve contenere solo numeri (massimo 15 cifre) con un "+" opzionale all\'inizio'
        }
      ],
      editorOptions: {
        onKeyPress: phoneNumberField,
        maxLength: 20,
      }
    },
    {
      dataField: "email", caption: "E-mail", filterOperations: ['contains'],
      validationRules: [
        {
          type: 'pattern',
          pattern: emailPattern,
          message: 'Inserisci un indirizzo email valido',
        },
        { type: 'required' }
      ],
    },
    {
      dataField: "country", caption: "Paese", allowFiltering: false, allowEditing: true,
      lookup: {
        dataSource: {
          store: countries,
          paginate: true
        },
        valueExpr: "id",
        displayExpr: e => `${e.iso_code} - ${e.name}`,
      },
      editorOptions: {
        showClearButton: true,
        searchEnabled: true,
      },
      async setCellValue(rowData, value) {
        rowData.disable_region = false;
        rowData.country = value;
        rowData.region = null;
        rowData.city = null;
        rowData.address = null;
      },
      validationRules: [{ type: 'required' }],
      visible: false,
    },
    {
      dataField: "country_display", caption: "Paese", allowFiltering: true, allowEditing: false, filterOperations: ['contains'],
    },
    {
      dataField: "region", caption: "Provincia/stato", allowFiltering: false, allowEditing: true,
      lookup: {
        dataSource: (options) => ({
          store: regions,
          filter: options.data ? ['country', '=', options.data.country] : null,
          paginate: true
        }),
        valueExpr: "id",
        displayExpr: e => e.code ? `${e.code} - ${e.name}` : e.name,
      },
      editorOptions: {
        showClearButton: true,
        searchEnabled: true,
      },
      async setCellValue(rowData, value, currentRowData) {
        rowData.region = value;
        rowData.city = null;
        rowData.address = null;
        if (!value) return;

        if (!currentRowData.country) {
          const selectedRegion = await regions.byKey(value);
          rowData.country = selectedRegion.country;
        }
      },
      validationRules: [{ type: 'required' }],
      visible: false,
    },
    {
      dataField: "region_display", caption: "Provincia/stato", allowFiltering: true, allowEditing: false, filterOperations: ['contains'],
    },
    {
      dataField: "city", caption: "Comune", allowFiltering: false, allowEditing: true,
      lookup: {
        dataSource: (options) => {
          let filter = null;
          if (options.data?.region)
            filter = ['region', '=', options.data.region];
          else if (options.data?.country)
              filter = ['country', '=', options.data.country];
              
          

          return {
            store: cities,
            filter: filter,
            paginate: true
          };
        },
        valueExpr: "id",
        displayExpr: e => e.postcode ? `${e.postcode} - ${e.name}` : e.name,
      },
      editorOptions: {
        showClearButton: true,
        searchEnabled: true,
      },
      async setCellValue(rowData, value, currentRowData) {
        rowData.disable_region = false;
        rowData.city = value;
        rowData.address = null;
        if (!value) return;

        if (!currentRowData.region) {
          const selectedCity = await cities.byKey(value);
          if (!selectedCity.region) {
            rowData.disable_region = true;
          } else {
            rowData.region = selectedCity.region;
          }
        } 
        if (!currentRowData.country) {
          if (rowData.disable_region) {
            const selectedRegion = await cities.byKey(rowData.city);
            rowData.country = selectedRegion.country;
          } else {
            const selectedRegion = await regions.byKey(rowData.region);
            rowData.country = selectedRegion.country;
          }
        }
      },
      validationRules: [{ type: 'required' }],
      visible: false,
    },
    {
      dataField: "city_display", caption: "Comune", allowFiltering: true, allowEditing: false, filterOperations: ['contains'],
    },
    {
      dataField: "address", caption: "Indirizzo", filterOperations: ['contains'],
      validationRules: [{ type: 'required' }],
      editorOptions: {
        maxLength: 50,
      }
    },
  ]
});
</script>

<template>
  <DxDataGrid v-bind="gridConfig" />
</template>