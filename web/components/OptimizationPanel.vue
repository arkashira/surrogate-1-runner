<template>
  <div class="optimization-panel">
    <h2>Cost Optimization Suggestions</h2>
    <ul>
      <li v-for="(recommendation, index) in optimizationRecommendations" :key="index">
        {{ recommendation }}
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState(['optimizationRecommendations']),
  },
};
</script>

<style scoped>
.optimization-panel {
  border: 1px solid #ccc;
  padding: 1rem;
  margin-bottom: 1rem;
}

.optimization-panel h2 {
  margin-top: 0;
}
</style>