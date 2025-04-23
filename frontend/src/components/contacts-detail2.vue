<script setup lang="js">
import djangoStore from '@/utils/django-adapter';
import {
    DxDataGrid, DxEditing, DxFilterRow, // Added DxFilterRow for consistency if needed
    DxForm,
    DxItem, // Import DxLookup if needed for specific editor customization, though often automatic
    DxPopup
} from 'devextreme-vue/data-grid';
import DxTabs from 'devextreme-vue/tabs';
import { ref } from 'vue'; // Import reactive

let selectedTab = ref(1)
/* eslint-disable */

// --- Data Stores ---
// Ensure djangoStore creates proper DevExtreme Data Stores (e.g., CustomStore)
const baseApiUrl = "http://localhost:8000/api/contacts";
const store = djangoStore(`${baseApiUrl}/contacts/`);
const citiesDataSource = djangoStore(`${baseApiUrl}/cities/`);
const countriesDataSource = djangoStore(`${baseApiUrl}/countries/`);
const regionsDataSource = djangoStore(`${baseApiUrl}/regions/`);

// --- Reactive state for dynamic filtering ---
// We don't strictly need this reactive object anymore if we use dataSource functions
// let currentFilters = reactive({
//     country: null,
//     region: null,
// });

// --- Dynamic DataSource Functions ---

// Function to get regions filtered by country
const getFilteredRegions = (options) => {
    // options.data contains the row data being edited
    const countryIsoCode = options?.data?.country;
    return {
        store: regionsDataSource,
        filter: countryIsoCode ? ['country', '=', countryIsoCode] : ['country', '=', null] // Filter by country or return none if no country
    };
};

// Function to get cities filtered by region
const getFilteredCities = (options) => {
    // options.data contains the row data being edited
    const regionId = options?.data?.region;
    return {
        store: citiesDataSource,
        filter: regionId ? ['region', '=', regionId] : ['region', '=', null] // Filter by region or return none if no region
    };
};


// --- Editor Preparing Handler ---
// Disables editors if the prerequisite field is not set
async function onEditorPreparing(e) {
    // Disable Region editor if Country is not set
    if (e.parentType === 'dataRow' && e.dataField === 'region') {
        // A country must be selected to enable region selection
        // Use the value during editing, which might differ from the initial row data
        const countryValue = e.editorOptions.value ?? e.row?.data?.country;
        e.editorOptions.disabled = !countryValue;
    }
    // Disable City editor if Region is not set
    else if (e.parentType === 'dataRow' && e.dataField === 'city') {
        // A region must be selected to enable city selection
        const regionValue = e.editorOptions.value ?? e.row?.data?.region;
        e.editorOptions.disabled = !regionValue;
    }
}

// --- Grid Columns Configuration ---
const columns = ref([ // Make columns reactive if needed, though usually not necessary unless columns change dynamically
    { dataField: "sede", caption: "Nome sede", filterOperations: ['contains'] },
    { dataField: "name", caption: "Ragione sociale", filterOperations: ['contains'] },
    {
        dataField: "country",
        caption: "Paese",
        lookup: {
            dataSource: countriesDataSource, // Direct source for countries
            valueExpr: "iso_code",
            displayExpr: "name",
        },
        // Reset Region and City when Country changes
        setCellValue: (rowData, value, currentRowData) => {
            rowData.country = value; // Set the new country value
            rowData.region = null;   // Reset region
            rowData.city = null;     // Reset city
          // currentRowData contains the original row data if needed
            return true
        }
    },
    {
        dataField: "region",
        caption: "Provincia/stato", // Make sure this matches your data model
        // visible: false, // Usually you want this visible in the form
        lookup: {
            dataSource: getFilteredRegions, // Use the dynamic function
            valueExpr: "id",
            displayExpr: "name",
        },
        // Reset City when Region changes
        setCellValue: (rowData, value, currentRowData) => {
            rowData.region = value; // Set the new region value
            rowData.city = null;    // Reset city

            // The original code tried setting country here based on region, which is backwards for cascading.
            // If your region data *includes* the country iso_code, you could potentially
            // auto-set the country if the user selects a region first, but that's not typical cascading.
            // Let's stick to the standard cascade: Country -> Region -> City
            // Example: If region object loaded contains country info:
            // if (value && typeof value === 'object' && value.country_iso_code) {
            //    rowData.country = value.country_iso_code; // Only if lookup returns the full object
            // }
        }
    },
    {
        dataField: "city",
        caption: "Comune",
        lookup: {
            dataSource: getFilteredCities, // Use the dynamic function
            valueExpr: "id",
            displayExpr: "name",
            // calculateDisplayValue might not be needed if valueExpr/displayExpr work correctly
            // calculateDisplayValue: (rowData) => { ... } // Remove or adjust if needed
        }
        // No setCellValue needed here as City is the last in the chain
    },

    { dataField: "phone", caption: "Telefono", filterOperations: ['contains'] },
    { dataField: "email", caption: "E-mail", filterOperations: ['contains'] },
]);
</script>

<template>
  <!-- Main Content Area -->
  <div class="content-area">
    <!-- Contacts Grid (conditionally rendered) -->
    <div v-if="selectedTab == 1" class="grid-container">
      <DxDataGrid
        :data-source="store"
        :show-borders="true"
        :remote-operations="true"
        :columns="columns"
        @editor-preparing="onEditorPreparing"
        key-expr="id"
        :repaint-changes-only="true"
        :allow-column-resizing="true"
        :column-auto-width="true"
      >
        <DxFilterRow :visible="true" />
        <DxEditing
          :allow-updating="true"
          :allow-adding="true"
          :allow-deleting="true"
          mode="popup"
          :use-icons="true"
        >
          <DxPopup
            :show-title="true"
            title="Contatto"
            :width="700"
            :height="525"
          />
          <DxForm>  
            <!-- Group General Info -->
            <DxItem
              :col-count="2"
              :col-span="2"
              item-type="group"
              caption="Informazioni Generali"
            >
              <DxItem data-field="name" />
              <DxItem data-field="sede" />
              <DxItem data-field="phone" />
              <DxItem data-field="email" />
            </DxItem>
            <!-- Group Address Info -->
            <DxItem
              :col-count="2"
              :col-span="2"
              item-type="group"
              caption="Indirizzo"
            >
              <DxItem data-field="country" />
              <DxItem data-field="region" />
              <DxItem data-field="city" />
              <!-- Add other address fields if they exist -->
            </DxItem>
          </DxForm>
        </DxEditing>
      </DxDataGrid>
    </div>

    <!-- Other Tabs Content (Example) -->
    <div v-if="selectedTab == 0">Profiles Content Here...</div>
    <div v-if="selectedTab == 2">Privacy Content Here...</div>
  </div>

  <!-- Tabs Navigation -->
  <div class="tabs-container">
    <DxTabs
      v-model:selected-index="selectedTab"
      :items="[{ text: 'Profiles' }, { text: 'Contacts' }, { text: 'Privacy' }]"
    />
  </div>
</template>

<style scoped>
.content-area {
  margin-bottom: 20px; /* Add some space between grid/content and tabs */
}

.grid-container {
  /* Add any specific styling for the grid container if needed */
}

.tabs-container {
  /* Styles for the tabs container */
  border-top: 1px solid #ccc; /* Example separator */
  padding-top: 10px;
}
</style>
