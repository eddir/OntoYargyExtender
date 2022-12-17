<template>
  <div>
    <CRow>
      <CCol md="12">
        <Ontologies></Ontologies>
        <NewOntologyFill></NewOntologyFill>
        <OntologiesTasks></OntologiesTasks>
      </CCol>
    </CRow>
  </div>
</template>

<script>

import Ontologies from "@/views/ontologies/Ontologies.vue";
import OntologiesTasks from "@/views/ontologies/OntologiesTasks.vue";
import NewOntologyFill from "@/views/ontologies/NewOntologyFill.vue";

export default {
  name: 'Dashboard',
  components: {Ontologies, NewOntologyFill, OntologiesTasks},
}
</script>
