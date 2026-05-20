
import Vue from 'vue'
import VueAxios from 'vue-axios'
import CostData from './costData'

Vue.use(VueAxios, axios)

export default new Vue({
  data: {
    costData: null
  },
  created() {
    this.costData = CostData.fetchCostData()
  }
})