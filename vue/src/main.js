import "babel-polyfill";
import Vue from 'vue'
import vueBraintree from 'vue-braintree'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.devtools = true;
Vue.use(vueBraintree)
Vue.use(VueAxios, axios);
Vue.axios.defaults.baseURL = process.env.API_BASE_URL;
Vue.axios.defaults.headers = {Pragma: 'no-cache'};

new Vue({
    el: '#app',
    render: h => h(App),
});
