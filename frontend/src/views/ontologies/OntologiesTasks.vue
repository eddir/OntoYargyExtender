<template>
  <CContainer>
    <CRow>
      <CCol>
        <CCard>
          <CCardHeader>Задачи</CCardHeader>
          <CCardBody>
            <CDataTable
                hover
                :items="tasks"
                :fields="tableFields"
                head-color="light"
                itemsPerPageSelect
                pagination
            >
              <timeago slot="date_created" slot-scope="{item}" :datetime="item.date_created"></timeago>
            </CDataTable>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  </CContainer>
</template>

<script>
import API from "@/services/API";

export default {
  name: "OntologiesTasks",
  data() {
    return {
      tasks: [],
      tableFields: [
        {key: 'id', label: 'ID'},
        {key: 'date_created', label: 'Время'},
        {key: 'status', label: 'Статус'},
      ]
    }
  },
  created() {
    API.getOntologiesTasks().then(response => {
      this.tasks = response.data.response;
    });
  }
}
</script>

<style scoped>

</style>
