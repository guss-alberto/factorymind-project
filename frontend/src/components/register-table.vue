<script setup lang="js">
import {
    DxDataGrid, DxFilterRow, DxEditing, DxPaging, DxPager, DxForm, DxPopup, DxItem
} from 'devextreme-vue/data-grid';
import djangoStore from '@/utils/django-adapter';
import axios from 'axios';
import { phonePattern, emailPattern, phoneNumberField } from '@/utils/validation-patterns';

/* eslint-disable */

const store = djangoStore("http://localhost:8000/api/contacts/register")

const columns = [
    {
        dataField: "first_name",
        caption: "Nome",
        validationRules: [{ type: 'required' }]
    },
    {
        dataField: "last_name",
        caption: "Cognome",
        validationRules: [{ type: 'required' }]
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
            {
                type: 'required'
            }
        ],
        editorOptions: { 
            onKeyPress: phoneNumberField
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
            }
        ],
        editorOptions: { 
            onKeyPress: phoneNumberField
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
                        id: data ? data.id : null // Includi l'ID per escludere il record corrente durante l'update
                    });
                    return response.data.available; // L'API resituisce { available: true/false }
                },
                message: 'Indirizzo email già registrato'
            },
            {
                type: 'required'
            }
        ]
    },
]
</script>

<template>
    <DxDataGrid :data-source="store" :show-borders="true" :remote-operations="true" :columns="columns">
        <DxPaging :enabled="true" />
        <DxPager :visible="true" :show-page-size-selector="true" :allowed-page-sizes="[2, 5, 10, 20]" />
        <dx-filter-row :visible="true" />
        <DxEditing :allow-updating="true" :allow-adding="true" :allow-deleting="true" mode="popup">
            <DxPopup :show-title="true" title="Contatto" />
            <DxForm>
                <DxItem :col-count="2" :col-span="2" item-type="group" caption="Nome">
                    <DxItem data-field="first_name" :editor-options="{ showClearButton: true, searchEnabled: true }"/>
                    <DxItem data-field="last_name" :editor-options="{ showClearButton: true, searchEnabled: true }"/>
                </DxItem>
                <DxItem :col-count="2" :col-span="2" item-type="group" caption="Contatti">
                    <DxItem data-field="phone" :editor-options="{ showClearButton: true, searchEnabled: true }"/>
                    <DxItem data-field="mobile" :editor-options="{ showClearButton: true, searchEnabled: true }"/>
                    <DxItem data-field="email" :editor-options="{ showClearButton: true, searchEnabled: true }"/>
                </DxItem>
            </DxForm>
        </DxEditing>
    </DxDataGrid>
</template>