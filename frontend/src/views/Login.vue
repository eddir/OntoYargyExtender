<template>
  <div class="c-app flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="6">
          <CCard class="p-4">
            <CCardHeader><h1>Вход</h1></CCardHeader>
            <CCardBody>
              <CAlert color="primary">Требуется авторизация.</CAlert>
              <CInput :value.sync="login" label="Логин"/>
              <CInput :value.sync="password" label="Пароль" type="password"/>
              <CButton color="success" class="m-2" @click="auth">Войти</CButton>
              <span class="float-right">
                  Нет аккаунта?
                  <CButton class="m-2 btn-link" to="/register">Зарегистрируйтесь</CButton>
                </span>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>

<script>
import Auth from "@/services/Auth";

export default {
  name: "Login",
  data() {
    return {
      login: "admin",
      password: "admin"
    }
  },
  methods: {
    auth() {
      Auth.credentialsLogin({'login': this.login, 'password': this.password})
    }
  }
}
</script>
