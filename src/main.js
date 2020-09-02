import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import Chat from 'vue-beautiful-chat';
import VueFormGenerator from "vue-form-generator/dist/vfg-core.js";
import "vue-form-generator/dist/vfg-core.css";
import store from './store'

Vue.config.productionTip = false
Vue.use(Chat)
Vue.use(VueFormGenerator)
new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
