<template>
  <CRow>
    <CCol md="12">
      <Ontologies :onto_list="onto_list"></Ontologies>
    </CCol>
  </CRow>
</template>

<script>
import API from "@/services/API.vue";
import Ontologies from "@/views/ontologies/Ontologies.vue";

export default {
  name: "FillerArchive",
  components: {Ontologies},
  data() {
    return {
      onto_list: [],
    }
  },
  created() {
    this.update();
  },
  methods: {
    update() {
      API.getFillOntologies().then(response => {
        this.onto_list = response.data.response;
      });
    }
  }
}
</script>

<style scoped>

</style>
