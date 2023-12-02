import  { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import axios from 'axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'


axios.defaults.baseURL = "http://127.0.0.1:8000"
const app= createApp(App);
app.config.globalProperties.$store = store;
app.provide("$store", store);
app.use(store).use(router).mount('#app');