<template>
  <CCard>
    <CCardHeader>Заявки</CCardHeader>
    <CCardBody>
      <CDataTable
          hover
          :items="requests"
          :fields="requestFields"
          head-color="light"
          :itemsPerPageSelect="{label: 'Элементов на странице', values: [5, 10, 20, 50]}"
          pagination
      >
        <template v-slot:no-items-view>
          <tr></tr>
        </template>
        <CButton slot="control-accept" slot-scope="{item}"
                 class="align-middle control-icon" style="margin-top: 10px"
                 color="success" size="sm"
                 @click="accept(item.request_id)">V
        </CButton>
        <CButton slot="control-reject" slot-scope="{item}"
                 class="align-middle control-icon" style="margin-top: 10px"
                 color="danger" size="sm"
                 @click="reject(item.request_id)">X
        </CButton>
      </CDataTable>
    </CCardBody>
  </CCard>
</template>

<script>
import API from "@/services/API.vue";
import Action from "@/services/Action.vue";

export default {
  name: "Requests",
  data() {
    return {
      requests: [],
      requestFields: [
        {key: 'username', label: 'Никнейм'},
        {key: 'name', label: 'Имя'},
        {key: 'email', label: 'Почта'},
        {key: 'organization', label: 'Организация'},
        {key: 'position', label: 'Должность'},
        {key: 'goal', label: 'Цель'},
        {key: 'control-accept', label: '', sorter: false, filter: false},
        {key: 'control-reject', label: '', sorter: false, filter: false},
      ]
    }
  },
  created() {
    this.update();
  },
  methods: {
    update() {
      API.getRequests().then(response => {
        this.requests = response.data.response;
      });
    },
    accept(request_id) {
      Action.quickAction("accept_request", request_id, () => {
        this.update();
      });
    },
    reject(request_id) {
      if (confirm("Вы уверены, что хотите отклонить заявку?")) {
        Action.quickAction("reject_request", request_id, () => {
          this.update();
        });
      }
    }
  }
}
</script>

<style scoped>

</style>
