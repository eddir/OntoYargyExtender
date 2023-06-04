<template>
  <div class="d-flex align-items-center min-vh-100">
    <CContainer fluid>
      <CRow class="justify-content-center">
        <CCol md="8">
          <CCard class="mx-4 mb-0">
            <CCardBody class="p-4">
              <div v-if="submitted">
                <h1>Регистрация</h1>
                <div class="d-flex justify-content-center">
                  <CIcon name="cil-check-circle" size="xl" class="text-success" style="height: 100px; width: 100px;"/>
                </div>
                <br/>
                <p class="text-muted">Спасибо за регистрацию! Ваша заявка отправлена на рассмотрение.</p>
              </div>
              <CForm @submit="register" v-else>
                <h1>Регистрация</h1>
                <p class="text-muted">Создайте свой аккаунт, чтобы запросить доступ к сервису.</p>
                <CInput
                    placeholder="Имя"
                    autocomplete="name"
                    v-model="firstName"
                    required
                >
                  <template #prepend-content>
                    <CIcon name="cil-user"/>
                  </template>
                </CInput>
                <CInput
                    placeholder="Фамилия"
                    autocomplete="family-name"
                    v-model="lastName"
                >
                  <template #prepend-content>
                    <CIcon name="cil-user"/>
                  </template>
                </CInput>
                <CInput
                    placeholder="Электронная почта"
                    autocomplete="email"
                    prepend="@"
                    v-model="email"
                    required
                />
                <CInput
                    placeholder="Никнейм"
                    autocomplete="username"
                    v-model="username"
                >
                  <template #prepend-content>
                    <CIcon name="cil-user"/>
                  </template>
                </CInput>
                <CInput
                    placeholder="Пароль"
                    type="password"
                    autocomplete="new-password"
                    v-model="password"
                    required
                >
                  <template #prepend-content>
                    <CIcon name="cil-lock-locked"/>
                  </template>
                </CInput>
                <CInput
                    placeholder="Повторите пароль"
                    type="password"
                    autocomplete="new-password"
                    v-model="repeatPassword"
                    required
                    :isValid="password === repeatPassword"
                >
                  <template #prepend-content>
                    <CIcon name="cil-lock-locked"/>
                  </template>
                </CInput>
                <CInput
                    placeholder="Компания"
                    autocomplete="organization"
                    v-model="organization"
                    required
                >
                  <template #prepend-content>
                    <CIcon name="cil-building"/>
                  </template>
                </CInput>
                <CInput
                    placeholder="Должность"
                    autocomplete="position"
                    v-model="position"
                    required
                >
                  <template #prepend-content>
                    <CIcon name="cil-briefcase"/>
                  </template>
                </CInput>
                <CSelect v-model="goal" :isValid="goal != null" :options="[
                      {value: null, label: 'Выберите цель'},
                      {value: 'research', label: 'Исследование'},
                      {value: 'development', label: 'Разработка'},
                      {value: 'marketing', label: 'Маркетинг'},
                      {value: 'other', label: 'Другое'}
                  ]">
                  <template #prepend-content>
                    <CIcon name="cil-location-pin"/>
                  </template>
                </CSelect>
                <CButton color="success" block type="submit">Создать аккаунт</CButton>
              </CForm>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>

<script>
import API from "@/services/API.vue";

export default {
  name: 'Register',
  data: () => {
    return {
      submitted: false,
      firstName: 'Eduard',
      lastName: 'R.',
      email: 'ea@rostkov.me',
      username: 'eddir',
      password: 'qwerty',
      repeatPassword: 'qwerty',
      organization: 'Google',
      position: 'CEO',
      goal: 'marketing',
    }
  },
  watch: {
    email: function (newEmail) {
      this.username = newEmail.split('@')[0]
    }
  },
  methods: {
    register(event) {
      this.$toast.info('Регистрация...')
      const form = event.currentTarget
      event.preventDefault()
      if (form.checkValidity() === false) {
        event.stopPropagation()
      } else {
        API.register({
          'first_name': this.firstName,
          'last_name': this.lastName,
          'email': this.email,
          'username': this.username,
          'password': this.password,
          'organization': this.organization,
          'position': this.position,
          'goal': this.goal,
        }).then(response => {
          if (response.data.code === 0) {
            this.$toast.success('Аккаунт создан. В ближайшее время с вами свяжется администратор по ' +
                'указанному адресу электронной почты.')
            this.submitted = true;
            return true;
          } else {
            this.$toast.error(response.data.response);
            return false;
          }
        })
      }
    }
  }
}
</script>
