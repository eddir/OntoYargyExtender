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
                <CInput :value.sync="input.name" label="Имя" placeholder="Имя"/>
              </CCol>
              <CCol sm="6">
                <CInput :value.sync="input.url" label="Адрес" placeholder="Ссылка на ресурс"/>
              </CCol>
              <CCol sm="6">
                <CSelect
                    :value.sync="input.parser"
                    label="Парсер"
                    :options="[
                      { label: 'RAD1', value: 'RAD1' },
                    ]"
                />
              </CCol>
              <CCol sm="6">
                <CSelect
                    label="Онтология"
                    :options="[
                      { label: 'ma-ont', value: 'RAD1' },
                    ]"
                />
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
  name: "NewOntology",
  data() {
    return {
      input: {
        name: "Радищевский музей",
        parser: "RAD1",
        url: "http://artkatalog.radmuseumart.ru/ru/"
      }
    }
  },
  created() {
  },
  methods: {
    send() {
      Action.formAction("import_ontology", this.input);
    },
  },
}
</script>
