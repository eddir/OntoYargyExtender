<script>
import API from "@/services/API.vue"
import Vue from "vue";

export default {
  name: "Action",
  mixins: [API],
  /**
   * Действие не требующее особой обработки. Выполняется по общему алгоритму.
   * @param response http запрос
   * @param callback действие после выполнения
   * @returns {*}
   */
  action(response, callback) {
    return response
        .then(function (response) {
          Vue.$toast.success(response.data.response);
          try {
            callback();
          } catch (e) {
            Vue.$toast.error(e);
            console.log("Callback error: " + e);
          }
        })
        .catch(function (error) {
          console.log(error);
          if (error.response.status === 500) {
            let messages = error.response.data.response;
            if (typeof messages === 'string') {
              Vue.$toast.error(messages);
              console.log("Error message: " + messages);
            } else {
              for (const [field, values] of Object.entries(messages)) {
                if (typeof values === 'string') {
                  Vue.$toast.error(values);
                  console.log("Error: " + values);
                } else {
                  values.forEach(message => {
                    Vue.$toast.error(field + ": " + message);
                    console.log("error: " + field + ": " + message);
                  });
                }
              }
            }

          }
        });
  },
  quickAction(action, unit_id, callback = () => null) {
    try {
      switch (action) {
        case "version":
          this.action(API.getVersion(), callback);
          break;
        case "remove_user":
          this.action(API.removeUser(unit_id), callback);
          break;
        case "accept_request":
          this.action(API.acceptRequest(unit_id), callback);
          break;
        case "reject_request":
          this.action(API.rejectRequest(unit_id), callback);
          break;
        default:
          console.error("Given action '" + action + "' is not defined in quickAction.");
      }
    } catch (e) {
      Vue.$toast.error(e.message);
    }
  },
  formAction(action, formData, callback = () => null) {
    switch (action) {
      case "create_user":
        this.action(API.addUser(formData), callback);
        break;
      case "import_ontology":
        this.action(API.importOntology(formData), callback);
        break;
      default:
        throw new Error("Given action '" + action + "' is not defined in formAction.");
    }
  },
  fileAction(action, formData, successCallback = () => null) {
    switch (action) {
      case "fill_ontology":
        this.action(API.fillOntology(formData.owl, formData.text), successCallback);
        break;
      default:
        throw new Error("Given action '" + action + "' is not defined in fileAction.");
    }
  },
}
</script>
