import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'
import './index.css'


router.afterEach(Swal.close)
createApp(App).use(router).mount('#app')

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

//Vue.use(VueSocketio,'http://127.0.0.1:80');
