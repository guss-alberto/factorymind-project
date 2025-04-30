<script setup lang="js">
import {
    DxDataGrid, DxFilterRow, DxEditing, DxPaging, DxPager, DxForm, DxPopup, DxItem, DxMasterDetail
} from 'devextreme-vue/data-grid';
import djangoStore from '@/utils/django-adapter';
import axios from 'axios';
import { phonePattern, emailPattern, phoneNumberField, vatPattern } from '@/utils/validation-patterns';
import ContactsDetail from './contacts-detail.vue';

const store = djangoStore("http://localhost:8000/api/contacts/register")

const columns = [
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
                        id: data ? data.id : null // includi id per escludere il record corrente durante l'update
                    });
                    return response.data.available; // API resituisce { available: true/false }
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
]
</script>

<template>
    <DxDataGrid :data-source="store" :show-borders="true" :remote-operations="true" :columns="columns">
        <DxPaging :enabled="true" />
        <DxPager :visible="true" :show-page-size-selector="true" :allowed-page-sizes="[2, 5, 10, 20]" />
        <dx-filter-row :visible="true" />
        <DxMasterDetail :enabled="true" template="masterDetailTemplate" />
        <template #masterDetailTemplate="{ data }">
            <ContactsDetail :id="data.data.id" />
        </template>
        <DxEditing :allow-updating="true" :allow-adding="true" :allow-deleting="true" mode="popup">
            <DxPopup :show-title="true" title="Anagrafica" />
            <DxForm>
                <DxItem :col-count="2" :col-span="2" item-type="group" caption="Identificativo">
                    <DxItem data-field="last_name" />
                    <DxItem data-field="first_name" />
                </DxItem>
                <DxItem :col-count="2" :col-span="2" item-type="group" caption="Contatti">
                    <DxItem data-field="phone" />
                    <DxItem data-field="phone_ext" />
                    <DxItem data-field="mobile" />
                    <DxItem data-field="email" />
                    <DxItem data-field="vat_number" />
                </DxItem>
            </DxForm>
        </DxEditing>
    </DxDataGrid>
</template>