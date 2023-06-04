<script>
import Vue from "vue";
import axios from 'axios';
import './AuthInterceptor';

let debugMode = window.location.href.indexOf("localhost") >= 0;

// const SERVER_URL = "https://localhost/"; // todo: change into proxy in vue.config.js
const SERVER_URL = "/";
const REST_URL = `${SERVER_URL}api/`;

export default {
  name: "API",
  AUTH_TELEGRAM_BOT: debugMode ? "RostkovBot" : "HostPanelRobot",
  SERVER_URL,
  REST_URL,
  getVersion() {
    return axios.get(`${REST_URL}version/`);
  },
  getUsers() {
    return axios.get(`${REST_URL}users/`);
  },
  addUser(formData) {
    return axios.post(`${REST_URL}users/create/`, formData);
  },
  removeUser(user_id) {
    return axios.delete(`${REST_URL}users/${user_id}/remove/`);
  },
  importOntology(formData) {
    return axios.post(`${REST_URL}ontologies/import/`, formData);
  },
  fillOntology(owl, text) {
    let formData = new FormData();
    formData.append("owl", owl);
    formData.append("text", text);
    return this.uploadFiles(`${REST_URL}ontologies/fill/`, formData);
  },
  getOntologies() {
    return axios.get(`${REST_URL}ontologies/`);
  },
  getFillOntologies() {
    return axios.get(`${REST_URL}ontologies/fill/`);
  },
  getOntologiesTasks() {
    return axios.get(`${REST_URL}ontologies/tasks/`);
  },
  downloadOntology(ontology_id) {
    window.open(`${REST_URL}ontologies/${ontology_id}/download/`);
  },
  downloadFilledOntology(ontology_id) {
    window.open(`${REST_URL}ontologies/fill/${ontology_id}/download/`);
  },
  uploadFiles(url, formData, progressCallback) {
    console.log("Uploading files...", formData);
    return axios.post(url, formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: progressCallback,
        },
    );
  },
  login(user) {
    axios.post(`${SERVER_URL}auth/credentials/login/`, user).then().catch(err => {
      Vue.$toast.error(err.response);
    })
  },
  register(user) {
    return axios.post(`${SERVER_URL}auth/credentials/register/`, user);
  },
  ping() {
    return axios.get(`${REST_URL}ping/`);
  },
  getSubs() {
    return axios.get(`${REST_URL}subscribers/`);
  },
  addSub(sub_data) {
    return axios.post(`${REST_URL}subscribers/`, sub_data);
  },
  removeSub(sub) {
    return axios.delete(`${REST_URL}subscribers/${sub['id']}/`);
  }
}
</script>
