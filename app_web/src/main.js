// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from "./store"
import ElementUI from 'element-ui'
import $ from 'jquery'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false;
Vue.use(ElementUI,{size:"mini"});
Vue.prototype.app_url = "http://127.0.0.1:8888";
Vue.prototype.$ = $;

let vue = new Vue({
  router,
  store: store,
  render: h => h(App),
}).$mount('#app');

export default vue;
