import Vue from "vue";
import App from "./App.vue";
import router from "./router";
//Bootstrap modules
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import VueMathjax from "vue-mathjax";

import { store } from "./store";

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(VueMathjax);

new Vue({
  store,
  router,
  render: (h) => h(App),
}).$mount("#app");
