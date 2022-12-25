<template>
  <CContainer>
    <CRow>
      <CCol>
        <CCard>
          <CCardHeader>Онтологии</CCardHeader>
          <CCardBody>
            <CDataTable
                hover
                :items="onto_list"
                :fields="tableFields"
                head-color="light"
                itemsPerPageSelect
                pagination
                :sorterValue="{ column: 'id', asc: false }"
            >
              <CButton slot="control-download" slot-scope="{item}"
                       color="primary" size="sm" style="margin-top: 10px"
                       @click="download(item.id)" v-show="item.status === 'done'">Скачать</CButton>
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
  name: "Ontologies",
  props: {
    onto_list: [],
  },
  data() {
    return {
      tableFields: [
        {key: 'id', label: 'Id'},
        {key: 'created_at', label: 'Дата создания'},
        {key: 'name', label: 'Название'},
        {key: 'status', label: 'Состояние', formatter: this.statusFormatter},
        {key: 'control-download', label: '', sorter: false, filter: false},
      ]
    }
  },
  methods: {
    download(ontology) {
      API.downloadFilledOntology(ontology);
    }
  },
}
</script>

<style scoped>

</style>
