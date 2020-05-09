import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from '../App.vue'
import Menu from '../components/Menu.vue'
import routerrrr from '../router/routes.js'
import VueRouter from "vue-router"
import DataExample from '../views/DataExample.vue'
import Header from '../components/Header.vue'

import axios from 'axios';
Vue.prototype.$axios = axios;

Vue.use(ElementUI)
Vue.use(VueRouter)

new Vue({
  el: '#app',
  router: routerrrr,
  render: h => h(App)
})

new Vue({
  el: '#menu',
  router: routerrrr,
  render: h => h(Menu)
})
