<template>
  <CContainer>
    <CRow>
      <CCol md="6">
        <CCard>
          <CCardHeader>OntoYargyExtender</CCardHeader>
          <CCardBody>
            <p><b>Версия:</b> {{ version }}</p>
          </CCardBody>
        </CCard>
        <CCard>
          <CCardHeader>Debug</CCardHeader>
          <CCardBody>
            <CButton variant="ghost" color="success" class="m-2" @click="ping">Ping</CButton>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  </CContainer>
</template>

<script>
import API from "@/services/API";
import Action from "@/services/Action";
import Vue from "vue";
import Subscribers from "@/views/settings/Subsсribers";

export default {
  name: "Settings",
  components: {Subscribers},
  data() {
    return {
      version: null
    }
  },
  created() {
    API.getVersion().then(response => this.version = response.data.response);
  },
  methods: {
    ping() {
      API.ping().then(response => Vue.$toast.success(response.data.response));
    }
  },
}
</script>

<style scoped>

</style>
