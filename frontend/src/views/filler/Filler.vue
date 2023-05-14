<template>
  <div>
    <CRow>
      <CCol ref="filler" md="12">
        <NewOntologyFill @update="start"></NewOntologyFill>
      </CCol>
      <Loader ref="wip"></Loader>
    </CRow>
  </div>
</template>
<script>
import NewOntologyFill from "@/views/ontologies/NewOntologyFill.vue";
import API from "@/services/API.vue";
import Loader from "@/views/base/Loader.vue";

export default {
  name: 'Filler',
  components: {NewOntologyFill, Loader},
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
      this.$refs.wip.show();
    },
    finish(ontology_id) {
      this.$refs.filler.hidden = false;
      this.$refs.wip.hide();
      this.$toast.success("Онтология заполнена");
      API.downloadFilledOntology(ontology_id)
    },
  }
}
</script>
