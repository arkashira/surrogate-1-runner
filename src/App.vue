
<template>
  <div id="app">
    <CostTrendChart :costData="costData" />
    <!-- Filter providers dropdown -->
  </div>
</template>

<script>
import CostTrendChart from './components/CostTrendChart.vue'

export default {
  components: {
    CostTrendChart
  },
  data() {
    return {
      costData: this.$root.$data.costData
    }
  }
}
</script>