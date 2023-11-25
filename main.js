import Vue from "vue";
import VueResource from "vue-resource";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import App from "./App.vue";

Vue.config.productionTip = false;

Vue.use(VueResource);
Vue.use(Antd);

new Vue({
  render: h => h(App)
}).$mount("#app");
