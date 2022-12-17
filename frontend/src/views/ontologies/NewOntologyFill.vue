<template>
  <CContainer>
    <CRow>
      <CCol md="12">
        <CCard>
          <CCardHeader>
            Импортировать
          </CCardHeader>
          <CCardBody>
            <CRow>
              <CCol sm="6">
                <CInputFile :value.sync="input.owl" label="OWL" placeholder="Исходная онтология"/>
              </CCol>
              <CCol sm="6">
                <CInputFile :value.sync="input.owl" label="Факты" placeholder="Факты для наполнения"/>
              </CCol>
            </CRow>
            <CButton key="send" color="success" class="m-2" @click="send">Начать</CButton>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  </CContainer>
</template>

<script>
import Action from "@/services/Action";

export default {
  name: "NewOntologyFill",
  data() {
    return {
      input: {
        owl: "",
        facts: ""
      }
    }
  },
  methods: {
    send() {
      Action.formAction("fill_ontology", this.input);
    },
  },
}
</script>
