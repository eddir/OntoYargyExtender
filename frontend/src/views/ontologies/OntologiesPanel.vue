<template>
  <div>
    <CRow>
      <CCol md="12">
        <Ontologies></Ontologies>
        <NewOntology></NewOntology>
        <OntologiesTasks></OntologiesTasks>
      </CCol>
    </CRow>
  </div>
</template>

<script>
import Ontologies from "@/views/ontologies/Ontologies"
import NewOntology from "@/views/ontologies/NewOntology";
import OntologiesTasks from "@/views/ontologies/OntologiesTasks";

export default {
  name: "OntologiesPanel",
  components: {Ontologies, NewOntology, OntologiesTasks},
}
</script>

<style scoped>

</style>
