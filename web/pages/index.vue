<template>
  <div class="login-container">
    <NForm label-position="top" :model="formModel" :rules="rules" ref="formRef">
      <NFormItem label="Email" path="email">
        <NInput
          v-model:value="formModel.email"
          placeholder="Digite seu email"
        />
      </NFormItem>
      <NFormItem label="Senha" path="password">
        <NInput
          v-model:value="formModel.password"
          type="password"
          placeholder="Digite sua senha"
        />
      </NFormItem>
      <NFormItem>
        <NButton type="primary" @click="handleSubmit" native-type="submit"
          >Entrar</NButton
        >
      </NFormItem>
    </NForm>
  </div>
</template>

<script setup lang="js">
import { NButton, NForm, NFormItem, NInput, useMessage } from 'naive-ui'
import { ref } from 'vue'

const formRef = ref(null);

const formModel = ref({
  email: '',
  password: ''
})
import { computed, defineComponent } from 'vue'
import { createDiscreteApi, darkTheme, lightTheme } from 'naive-ui'

const response = ref(null);
const error = ref(null);

const themeRef = ref('light')
const configProviderPropsRef = computed(() => ({
  theme: themeRef.value === 'light' ? lightTheme : darkTheme
}))

const { message, notification, dialog, loadingBar, modal } = createDiscreteApi(
  ['message', 'dialog', 'notification', 'loadingBar', 'modal'],
  {
    configProviderProps: configProviderPropsRef
  }
)

async function handleSubmit(e) {
  // console.log('Email:', formModel.value.email)
  // console.log('Senha:', formModel.value.password)
  e.preventDefault();

  await formRef.value?.validate(
    async (errors) => {
      if (errors) {
        return
      }

      const messageReactive = message.loading('Verifying', {
          duration: 0
      })

      await delay(2000);
      const { data, error: fetchError } = await useLazyFetch('http://127.0.0.1:8000/token', {
        method: 'POST',
        body:{
          // "username": "admin",
          // "password": "secret"
          "username": formModel.value.email,
          "password": formModel.value.password
        },
        headers: {
          'Content-Type': 'application/json'
      }
  });

  // Verificando e armazenando os resultados
  if (data.value !== null) {
    response.value = data;
    console.log(`data: ${data.value}`)
    console.log(data.value?.access_token)
    console.log(data.value?.token_type)
    message.success('logado com sucesso!')

    message.info(`Seu token de acesso é: ${data.value?.access_token}`)
  } else {
    message.error('Usuário não encontrado!')
  }

  // if (fetchError !== null) {
  //   error.value = fetchError;
  //   message.error('Ocorreu um erro ' ,error)
  //   console.log(`fetchError: ${error}`)
  // }

      messageReactive.destroy()
    }
  )
}

const rules = {
  email: [
    {
      required: true,
      message: 'Email é obrigatório',
      trigger: ['input', 'blur']
    }
  ],
  password: [
    {
      required: true,
      message: 'Password é obrigatório',
      trigger: ['input', 'blur']
    }
  ]
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
</script>

<style scoped>
.login-container {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.n-form-item {
  margin-bottom: 16px;
}

n-button {
  width: 100%;
}
</style>
