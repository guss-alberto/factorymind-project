<script setup lang="js">
import {
    DxDataGrid, DxFilterRow, DxEditing, DxPaging, DxPager, DxForm, DxPopup, DxItem, DxRequiredRule, DxPatternRule, DxEmailRule, DxAsyncRule
} from 'devextreme-vue/data-grid';
import djangoStore from '@/utils/django-adapter';
import { phonePattern, emailPattern } from '@/utils/validation-patterns';

const pattern = /^\d{10}$/  // pattern italiano 10 cifre

/* eslint-disable */

const store = djangoStore("http://localhost:8000/api/contacts/register")


const validateUniqueEmail = async ({ value, data }) => {
  try {
    // Verifica se l'email è stata modificata
    if (data && data.email === value) {
      return true; // Se l'email non è cambiata, non serve verificare
    }

    const response = await fetch("http://localhost:8000/api/contacts/register/check-email/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: value,
        id: data?.id || null // Includi l'ID per escludere il record corrente durante l'update
      }),
    });

    if (!response.ok) {
      throw new Error("Errore nella verifica dell'email");
    }

    const result = await response.json();
    return result.available; // L'API dovrebbe restituire { available: true/false }
  } catch (error) {
    console.error("Errore validazione email:", error);
    return false; // In caso di errore, considera l'email come non valida
  }
};

</script>



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
                message: 'Il telefono deve contenere solo numeri (massimo 15 cifre) con un "+" opzionale all\'inizio'
            }
        ]
    },
    { 
        dataField: "mobile", 
        caption: "Cellulare", 
        validationRules: [
            { 
                type: 'pattern', 
                pattern: phonePattern, 
                message: 'Il cellulare deve contenere solo numeri (massimo 15 cifre) con un "+" opzionale all\'inizio'
            },
        ]
    },
    { 
        dataField: "firstEmail", 
        caption: "E-mail primaria", 
        validationRules: [
            { 
                type: 'pattern', 
                pattern: emailPattern, 
                message: 'Inserisci un indirizzo email valido',
            },
            { 
                type:  'required'
            }
        ]
    },
    { 
        dataField: "secondEmail", 
        caption: "E-mail secondaria", 
        validationRules: [
            { 
                type: 'pattern', 
                pattern: emailPattern, 
                message: 'Inserisci un indirizzo email valido'
            },
            { 
                type: 'custom',
                validationCallback: function(options) {
                    return !options.value || emailPattern.test(options.value);
                },
                message: 'Inserisci un indirizzo email valido'
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
                <DxItem :col-count="2" :col-span="2" item-type="group">
                    <DxItem data-field="phone">
                        <DxRequiredRule />
                        <DxPatternRule
                            :pattern="pattern"
                            message="Il telefono deve avere il formato 0000000000"
                        />
                    </DxItem>
                    <DxItem data-field="Email">
                        <DxRequiredRule/>
                        <DxEmailRule/>
                        <DxAsyncRule
                        :validation-callback="validateUniqueEmail"
                        message="Email gia' registrata"
                        />
                    </=====
                <DxForm>
                    <DxItem :col-count="2" :col-span="2" item-type="group" caption="Informazioni">
                        <DxItem data-field="first_name" />
                        <DxItem data-field="last_name" />
                        <DxItem data-field="firstEmail" />
                        <DxItem data-field="secondEmail" />
                        <DxItem data-field="mobile" />
                        <DxItem data-field="phone" />
                    </DxItem>
                </DxForm>
                </DxItem>
            </DxForm>
        </DxEditing>
    </DxDataGrid>
</template>