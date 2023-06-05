<template>
  <CContainer>
    <CRow>
      <CCol>
        <users></users>
        <requests></requests>
      </CCol>
    </CRow>
  </CContainer>
</template>

<script>

export default {
  name: "UsersDashboard",
  components: {
    users: () => import('@/views/users/Users.vue'),
    requests: () => import('@/views/users/Requests.vue'),
  }
}
</script>

<style scoped>

</style>
