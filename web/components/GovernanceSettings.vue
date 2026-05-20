<template>
  <div>
    <h2>Governance Settings</h2>
    <form @submit.prevent="saveSettings">
      <div>
        <label>Model Cost Budget:</label>
        <input type="number" v-model="modelCostBudget" />
      </div>
      <div>
        <label>Alert Threshold:</label>
        <input type="number" v-model="alertThreshold" />
      </div>
      <div>
        <label>Token Usage Limit:</label>
        <input type="number" v-model="tokenUsageLimit" />
      </div>
      <button type="submit">Save Settings</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      modelCostBudget: null,
      alertThreshold: null,
      tokenUsageLimit: null,
    };
  },
  methods: {
    async saveSettings() {
      const settings = {
        modelCostBudget: this.modelCostBudget,
        alertThreshold: this.alertThreshold,
        tokenUsageLimit: this.tokenUsageLimit,
      };

      try {
        await axios.post('/api/policy', settings);
        alert('Settings saved successfully');
      } catch (error) {
        console.error('Error saving settings:', error);
        alert('Failed to save settings');
      }
    },
  },
};
</script>