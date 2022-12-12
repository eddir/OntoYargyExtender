<template>
  <CContainer>
    <CRow>
      <CCol>
        <CCard>
          <CCardHeader>Онтологии</CCardHeader>
          <CCardBody>
            <CDataTable
                hover
                :items="ontologies"
                :fields="tableFields"
                head-color="light"
                itemsPerPageSelect
                pagination
                :sorterValue="{ column: 'id', asc: false }"
            >
              <CButton slot="control-download" slot-scope="{item}" color="primary" size="sm" @click="download(item.id)">Скачать</CButton>
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
  data() {
    return {
      ontologies: [],
      tableFields: [
        {key: 'id', label: 'Id'},
        {key: 'name', label: 'Название'},
        {key: 'control-download', label: '', sorter: false, filter: false},
      ]
    }
  },
  methods: {
    download(ontology) {
      API.downloadOntology(ontology);
    }
  },
  created() {
    API.getOntologies().then(response => {
      this.ontologies = response.data.response;
    });
  }
}
</script>

<style scoped>

</style>
