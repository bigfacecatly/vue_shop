import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'

// 导入图标
import './assets/font/iconfont.css'
// 导入全局样式表
import './assets/css/global.css'

// 配置axios
import axios from 'axios'
axios.defaults.baseURL = 'http://127.0.0.1:8080/api/'
Vue.prototype.$http = axios

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
