<script setup lang="js">
import {
    DxDataGrid
} from 'devextreme-vue/data-grid';
import djangoStore from '@/utils/django-adapter';
import axios from 'axios';
import { phonePattern, emailPattern, phoneNumberField, vatPattern } from '@/utils/validation-patterns';
import RegisterTabs from './register-tabs.vue';
import {  createApp, ref } from 'vue';

const store = djangoStore("http://localhost:8000/api/contacts/register")
const registry_types = djangoStore("http://localhost:8000/api/contacts/register_type")

const gridConfig = ref({
    dataSource: store,
    remoteOperations: true,
    paging: { enabled: true },
    pager: {
        visible: true,
        showPageSizeSelector: true,
        allowedPageSizes: [2, 5, 10, 20],
    },
    filterRow: { visible: true },
        editing: {
        allowUpdating: true,
        allowAdding: true,
        allowDeleting: true,
        mode: "popup",
        popup: {
            showTitle: true,
            title: 'Anagrafica',
        },
        form: {
            items: [
                {
                itemType: "group",
                caption: "Identificativo",
                colCount: 2,
                colSpan: 2,
                items: ["last_name", "first_name", "registry_type"],
                },
                {
                itemType: "group",
                caption: "Contatti",
                colCount: 2,
                colSpan: 2,
                items: ["phone", "phone_ext", "mobile", "email", "vat_number"],
                },
            ]
        },
    },

    columns: [
    {
        dataField: "last_name",
        caption: "Cognome",
        validationRules: [{ type: 'required' }],
        editorOptions: {
            maxLength: 50,
        }
    },
    {
        dataField: "first_name",
        caption: "Nome",
        editorOptions: {
            maxLength: 50,
        }
    },
    {
        dataField: "phone",
        caption: "Telefono",
        validationRules: [
            {
                type: 'pattern',
                pattern: phonePattern,
                message: 'Il telefono deve contenere solo numeri con un "+" opzionale all\'inizio'
            },
        ],
        editorOptions: {
            onKeyPress: phoneNumberField,
            maxLength: 20,
        }
    },
    {
        dataField: "phone_ext",
        caption: "Telefono ext.",
        validationRules: [
            {
                type: 'pattern',
                pattern: phonePattern,
                message: 'Il telefono deve contenere solo numeri con un "+" opzionale all\'inizio'
            },
        ],
        editorOptions: {
            onKeyPress: phoneNumberField,
            maxLength: 20,
        }
    },
    {
        dataField: "mobile",
        caption: "Cellulare",
        validationRules: [
            {
                type: 'pattern',
                pattern: phonePattern,
                message: 'Il telefono deve contenere solo numeri con un "+" opzionale all\'inizio'
            },
        ],
        editorOptions: {
            onKeyPress: phoneNumberField,
            maxLength: 20,
        }
    },
    {
        dataField: "email",
        caption: "E-mail",
        validationRules: [
            {
                type: 'pattern',
                pattern: emailPattern,
                message: 'Inserisci un indirizzo email valido'
            },
            {
                type: 'async',
                validationCallback: async ({ value, data }) => {
                    const response = await axios.post("http://localhost:8000/api/contacts/register/check-email/", {
                        email: value,
                        id: data ? data.id : null // include id to exclude current record during update
                    });
                    return response.data.available; // API return { available: true/false }
                },
                message: 'Indirizzo email già registrato'
            },
            {
                type: 'required'
            }
        ]
    },
    {
        dataField: "vat_number",
        caption: "P.IVA",
        validationRules: [
            {
                type: 'pattern',
                pattern: vatPattern,
                message: 'Inserisci una P.IVA valida (Es. IT12345678912)',
            },
        ],
        editorOptions: {
            maxLength: 20,
        }
    },
    {
        dataField: "registry_type",
        caption: "Tipo Anagrafica",
        allowEditing: true,
        validationRules: [{ type: 'required' }],
        lookup: {
        dataSource: registry_types,
        valueExpr: "id",
        displayExpr: e => `${e.name}`,
        },
        editorOptions: {
            showClearButton: true,
            searchEnabled: true,
        },
        visible: false,
    },
    {
      dataField: "registry_type_display", caption: "Tipo Anagrafica", allowFiltering: true, allowEditing: false, filterOperations: ['contains'],
    },
    ],
    masterDetail: {
        enabled: true,
        component: RegisterTabs,
        template: (container, options) => {
            const contactDetailComponent = createApp(RegisterTabs, {
            id: options.data.id,  // pass id of the component to RegisterTab
            registry_type: options.data.registry_type_display,
        });
        contactDetailComponent.mount(container);
        }
    },
    onRowExpanding: function(e){
        e.component.collapseAll(-1);
    },
})
</script>

<template>
    <DxDataGrid v-bind="gridConfig" />
</template>