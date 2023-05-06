<template>
  <div>
    <CRow>
      <CCol ref="filler" md="12">
        <NewOntologyFill @update="start"></NewOntologyFill>
      </CCol>
      <CCol ref="wip" md="12" hidden>
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
    </CRow>
  </div>
</template>
<script>
import NewOntologyFill from "@/views/ontologies/NewOntologyFill.vue";
import API from "@/services/API.vue";

export default {
  name: 'Filler',
  components: {NewOntologyFill},
  data() {
    return {
      channel: null,
    }
  },
  created() {
    this.channel = this.$pusher.subscribe('ontologies-tasks');
    this.channel.bind('fill-event', data => {
      this.finish(data['ontology_id']);
    });
  },
  beforeDestroy() {
    this.channel.unbind();
    this.$pusher.unsubscribe('ontologies-tasks');
  },
  methods: {
    start() {
      this.$refs.filler.hidden = true;
      this.$refs.wip.hidden = false;
    },
    finish(ontology_id) {
      this.$refs.filler.hidden = false;
      this.$refs.wip.hidden = true;
      this.$toast.success("Онтология заполнена");
      API.downloadFilledOntology(ontology_id)
    },
  }
}
</script>
