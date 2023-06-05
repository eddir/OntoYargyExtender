<template>
  <CCard>
    <CCardHeader>Пользователи</CCardHeader>
    <CCardBody>
      <CDataTable
          hover
          :items="users"
          :fields="tableFields"
          head-color="light"
          :itemsPerPageSelect="{label: 'Элементов на странице', values: [5, 10, 20, 50]}"
          pagination
      >
        <template v-slot:no-items-view>
          <tr></tr>
        </template>
        <CButton slot="control-remove" slot-scope="{item}"
                 class="align-middle control-icon" style="margin-top: 10px"
                 color="danger" size="sm"
                 @click="remove(item.user_id)">X
        </CButton>
      </CDataTable>
      <router-link to="/users/add/">
        <CButton color="primary" size="sm">Добавить пользователя</CButton>
      </router-link>
    </CCardBody>
  </CCard>
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
      // first ask for confirmation
      if (confirm("Вы уверены, что хотите удалить пользователя?")) {
        Action.quickAction("remove_user", user_id, () => {
          API.getUsers().then(response => {
            this.users = response.data.response;
          });
        });
      }
    },
    test() {
      // тест одобрения заявки
      API.getRequests().then(response => {
        let requests = response.data.response;
        if (requests.length > 0) {
          let request_id = requests[0].request_id;
          API.acceptRequest(request_id).then(response => {
            console.log(response.data);
          });
        }
      });
    }
  }
}
</script>
