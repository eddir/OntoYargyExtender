<template>
  <div>
    <CRow>
      <CCol md="12">
        <Ontologies :onto_list="onto_list"></Ontologies>
        <NewOntologyFill @update="update"></NewOntologyFill>
      </CCol>
    </CRow>
  </div>
</template>

<script>

import Ontologies from "@/views/ontologies/Ontologies.vue";
import NewOntologyFill from "@/views/ontologies/NewOntologyFill.vue";
import API from "@/services/API.vue";

export default {
  name: 'Dashboard',
  components: {Ontologies, NewOntologyFill},
  data() {
    return {
      onto_list: [],
    }
  },
  created() {
    this.timer = setInterval(() => {
      API.getFillOntologies().then(response => {
        this.onto_list = response.data.response;
      });
    }, 3000)
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
