<template>
  <CContainer>
    <CRow>
      <CCol md="12">
        <CCard>
          <CCardHeader>
            Добавление пользователя в систему
          </CCardHeader>
          <CCardBody>
            <CRow>
              <CCol sm="6">
                <CInput :value.sync="input.first_name" label="Имя" placeholder="Имя"/>
              </CCol>
              <CCol sm="6">
                <CInput :value.sync="input.last_name" label="Фамилия" placeholder="Фамилия"/>
              </CCol>
              <CCol sm="6">
                <CInput :value.sync="input.username" label="Никнейм" placeholder="Логин"/>
              </CCol>
              <CCol sm="6">
                <CInput :value.sync="input.email" label="E-mail" placeholder="Электронная почта"/>
              </CCol>
              <CCol sm="6">
                <CInput :value.sync="input.password" label="Пароль" placeholder="Пароль"/>
              </CCol>
              <CCol sm="6">
                <CSelect
                    :value.sync="input.is_staff"
                    label="роль"
                    :options="[
                      { label: 'Администратор', value: true },
                      { label: 'Редактор', value: false },
                    ]"
                />
              </CCol>
            </CRow>
            <CButton key="send" color="success" class="m-2" @click="send">Создать</CButton>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  </CContainer>
</template>

<script>
import Action from "@/services/Action";

export default {
  name: "NewServer",
  data() {
    return {
      input: {
        first_name: "Иван",
        last_name: "Иванов",
        username: "iiv",
        email: "ivan@gmail.com",
        password: "123456",
        is_staff: false
      }
    }
  },
  created() {
  },
  methods: {
    send() {
      Action.formAction("create_user", this.input, () => window.location.href = '/#/users/');
    },
  },
}
</script>
