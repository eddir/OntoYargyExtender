<script>
import Vue from "vue";
import API from "@/services/API";
import Utils from "@/services/Utils";
import axios from "axios";

export default {
  name: "Auth",
  components: {API},
  credentialsLogin(user, redirectUrl = "/") {
    axios.post(`${API.SERVER_URL}auth/credentials/login/`, user).then(resp => {
      if (resp.data.code === 0) {
        Utils.setCookie("XCSRF-TOKEN", resp.data.response.csrf, 14);
        Vue.$toast.success("Авторизация пройдена!");
        window.location.href = redirectUrl;
      } else {
        Vue.$toast.error("Не удалось авторизоваться");
      }
    }).catch(err => {
      console.log(err);
    })
  },
  credentialsLogout() {
    axios.post(`${API.SERVER_URL}auth/credentials/logout/`).then(resp => {
      if (resp.data.code === 0) {
        Vue.$toast.success("Выход выполнен!");
      } else {
        Vue.$toast.error("Не удалось выйти");
      }
    }).catch(err => {
      console.log(err);
    })
  },
}
</script>
