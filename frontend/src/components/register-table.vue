<script setup lang="js">
import {
    DxDataGrid, DxFilterRow, DxEditing, DxPaging, DxPager, DxForm, DxPopup, DxItem, DxRequiredRule, DxPatternRule, DxEmailRule, DxAsyncRule
} from 'devextreme-vue/data-grid';
import djangoStore from '@/utils/django-adapter';

const pattern = /^\d{10}$/  // pattern italiano 10 cifre

const columns = [
    { dataField: "first_name", caption: "Nome", filterOperations: ['contains'] },
    { dataField: "last_name", caption: "Cognome", filterOperations: ['contains'] },
    { dataField: "phone", caption: "Telefono", filterOperations: ['contains'] },
    { dataField: "mobile", caption: "Cellulare", filterOperations: ['contains'] },
    { dataField: "email", caption: "E-mail", filterOperations: ['contains'] },
]

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
                    </DxItem>
                </DxItem>
            </DxForm>
        </DxEditing>
    </DxDataGrid>
</template>