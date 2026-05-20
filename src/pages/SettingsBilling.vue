<template>
  <section class="billing-settings">
    <h2>Billing Settings</h2>

    <!-- Loading / Error states -->
    <p v-if="loading" class="status">Loading billing information…</p>
    <p v-else-if="error" class="status error">{{ error }}</p>

    <!-- Billing details -->
    <div v-else class="billing-info">
      <p><strong>Current Plan:</strong> {{ status.planName }}</p>
      <p><strong>Next Renewal Date:</strong> {{ formattedRenewalDate }}</p>

      <!-- Upgrade button -->
      <button
        @click="upgradePlan"
        :disabled="upgrading"
        class="upgrade-btn"
      >
        {{ upgrading ? 'Redirecting…' : 'Upgrade' }}
      </button>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import axios from 'axios';

interface BillingStatus {
  planName: string;
  renewalDate: string; // ISO string
}

export default defineComponent({
  name: 'SettingsBilling',
  setup() {
    /* ------------------------------------------------------------------
     * State
     * ------------------------------------------------------------------ */
    const status = ref<BillingStatus>({ planName: '', renewalDate: '' });
    const loading = ref(true);
    const upgrading = ref(false);
    const error = ref<string | null>(null);

    /* ------------------------------------------------------------------
     * Computed
     * ------------------------------------------------------------------ */
    const formattedRenewalDate = computed(() => {
      if (!status.value.renewalDate) return 'N/A';
      const d = new Date(status.value.renewalDate);
      return d.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    });

    /* ------------------------------------------------------------------
     * API helpers
     * ------------------------------------------------------------------ */
    const fetchStatus = async () => {
      try {
        const { data } = await axios.get<BillingStatus>('/api/billing/status');
        status.value = data;
      } catch (e) {
        error.value = 'Failed to load billing status.';
      } finally {
        loading.value = false;
      }
    };

    const upgradePlan = async () => {
      upgrading.value = true;
      try {
        const { data } = await axios.post<{ url: string }>('/api/billing/checkout', {
          mode: 'subscription',
        });
        window.location.href = data.url; // Stripe Checkout
      } catch (e) {
        error.value = 'Failed to initiate upgrade.';
        upgrading.value = false;
      }
    };

    /* ------------------------------------------------------------------
     * Lifecycle
     * ------------------------------------------------------------------ */
    onMounted(fetchStatus);

    /* ------------------------------------------------------------------
     * Expose to template
     * ------------------------------------------------------------------ */
    return {
      status,
      loading,
      upgrading,
      error,
      formattedRenewalDate,
      upgradePlan,
    };
  },
});
</script>

<style scoped>
.billing-settings {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: system-ui, sans-serif;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.status {
  font-style: italic;
  color: #555;
}

.status.error {
  color: #d00;
}

.billing-info p {
  margin: 0.5rem 0;
}

.upgrade-btn {
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background: #0066ff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.upgrade-btn:disabled {
  background: #999;
  cursor: not-allowed;
}
</style>