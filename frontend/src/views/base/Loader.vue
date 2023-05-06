<template>
  <CCol md="12" ref="loader" hidden>
    <CContainer>
      <CRow>
        <CCol md="12">
          <CCard>
            <CCardHeader>
              Заполнение онтологий
            </CCardHeader>
            <CCardBody>
              <CSpinner
                  color="primary"
                  style="width:4rem;height:4rem;"
              />
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </CCol>
</template>

<script>
export default {
  name: "Loader",
  methods: {
    hide() {
      this.$refs.loader.hidden = true;
    },
    show() {
      this.$refs.loader.hidden = false;
    }
  }
}
</script>

<style scoped>

</style>
