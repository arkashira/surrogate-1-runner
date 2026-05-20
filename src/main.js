
import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'

Vue.use(axios)

const api = axios.create({
  baseURL: 'http://localhost:3000'
})

new Vue({
  render: h => h(App),
  data: {
    costData: null
  },
  created() {
    this.costData = CostData.fetchCostData()
  }
}).$mount('#app')