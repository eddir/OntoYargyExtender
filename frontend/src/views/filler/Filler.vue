<template>
  <div>
    <CRow>
      <CCol md="12">
        <NewOntologyFill @update="update"></NewOntologyFill>
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
      onto_list: [],
      channel: null,
    }
  },
  created() {
    this.channel = this.$pusher.subscribe('ontologies-tasks');
    this.channel.bind('fill-event', () => {
      this.update();
    });
    this.update();
  },
  beforeDestroy() {
    this.channel.unbind();
    this.$pusher.unsubscribe('ontologies-tasks');
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
