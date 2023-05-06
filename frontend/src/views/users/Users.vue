<template>
  <CContainer>
    <CRow>
      <CCol>
        <CCard>
          <CCardHeader>Пользователи</CCardHeader>
          <CCardBody>
            <CDataTable
                hover
                :items="users"
                :fields="tableFields"
                head-color="light"
                itemsPerPageSelect
                pagination
            >
                <CButton slot="control-remove" slot-scope="{item}"
                         class="align-middle control-icon" style="margin-top: 10px"
                         color="danger" size="sm"
                @click="remove(item.user_id)">X</CButton>
            </CDataTable>
            <router-link to="/users/add/">
              <CButton color="primary" size="sm">Добавить пользователя</CButton>
            </router-link>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  </CContainer>
</template>

<script>
import API from "@/services/API.vue";
import Action from "@/services/Action";

export default {
  name: "Users",
  data() {
    return {
      users: [],
      tableFields: [
        {key: 'username', label: 'Никнейм'},
        {key: 'name', label: 'Имя'},
        {key: 'email', label: 'Почта'},
        {key: 'control-remove', label: '', sorter: false, filter: false},
      ]
    }
  },
  created() {
    API.getUsers().then(response => {
      this.users = response.data.response;
    });
  },
  methods: {
    remove(user_id) {
      Action.quickAction("remove_user", user_id, () => {
        API.getUsers().then(response => {
          this.users = response.data.response;
        });
      });
    }
  }
}
</script>
