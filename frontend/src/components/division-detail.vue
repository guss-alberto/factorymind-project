<style scoped>
.success-message {
  color: green;
  font-weight: bold;
}

.error-message {
  color: red;
  font-weight: bold;
}
</style>I

<script setup lang="js">
import djangoStore from '@/utils/django-adapter';
import {DxForm} from 'devextreme-vue/form';

import { defineProps, ref } from 'vue';

const props = defineProps(["id"]); 

const suppliers = djangoStore("http://localhost:8000/api/contacts/suppliers/", {excluded_id: props.id});
const divisions = djangoStore("http://localhost:8000/api/contacts/divisions");


const formData = ref({  
  client: props.id,
  code: '',
  name: '',
  supplier: null,
});

const formRef = ref(null);
const message = ref("");

const handleSubmit = async () => {
  const formInstance = formRef.value.instance;
  if (formInstance.validate().isValid) {
    try {
      await divisions.insert(formData.value);
      message.value = 'Dati invitati con successo';
    } catch (error) {
      message.value = `Errore: ${error.message}`;
    }
  }
};

const formConfig = ref([
    {
      dataField: 'code',
      editorType: 'dxTextBox',
      label: { text: 'Codice' },
      validationRules: [{ type: 'required' }],
    },
    {
      dataField: 'name',
      editorType: 'dxTextBox',
      label: { text: 'Nome' },
      validationRules: [{ type: 'required' }],
    },
    {
      dataField: "supplier",
      label: { text: "Fornitore" },
      editorType: "dxSelectBox",
      editorOptions: {
        dataSource: suppliers,
        valueExpr: "id",
        displayExpr: item => item ? `${item.last_name} ${item.first_name}` : '',
        searchEnabled: true,
        showClearButton: true,
      },
      
      validationRules: [{ type: 'required' }],
    },
    {
      itemType: "simple",
      editorType: "dxButton",
      editorOptions: {
        text: "Invia",
        type: "default",
        onClick: handleSubmit,
      },  
    }
  ]
);

</script>

<template>
  <div v-if="message" :class="{'success-message': message.includes('successo'), 'error-message': message.includes('Errore')}">
    {{ message }}
  </div>
  <DxForm ref="formRef" :formData="formData" :items="formConfig" />
</template>