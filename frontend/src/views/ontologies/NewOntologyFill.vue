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
                <CInputFile @change="selectOWL" label="OWL" placeholder="Исходная онтология"/>
              </CCol>
              <CCol sm="6">
                <CInputFile @change="selectFacts" label="Текст" placeholder="Исходный текст"/>
              </CCol>
            </CRow>
            <CButton key="send" color="primary" class="m-2" @click="send">Начать</CButton>
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
        text: ""
      }
    }
  },
  methods: {
    selectOWL(files) {
      this.input.owl = files[0];
    },
    selectFacts(files) {
      this.input.text = files[0];
    },
    send() {
      if (!this.input.owl) {
        this.$toast.error("Не выбрана исходная онтология");
      }
      if (!this.input.text) {
        this.$toast.error("Не выбраны факты");
      }
      if (this.input.owl && this.input.text) {
        Action.fileAction("fill_ontology", this.input, () => {
          this.$emit("update");
        });
      }
    },
  },
}
</script>
