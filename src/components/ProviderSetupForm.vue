<template>
  <form @submit.prevent="handleSubmit" class="provider-setup-form">
    <h2>Add Cloud Provider Credentials</h2>

    <label for="provider">Provider</label>
    <select id="provider" v-model="provider" required>
      <option disabled value="">Select provider</option>
      <option value="aws">AWS</option>
      <option value="gcp">GCP</option>
      <option value="azure">Azure</option>
    </select>

    <!-- AWS fields -->
    <div v-if="provider === 'aws'" class="provider-fields">
      <label for="aws-access-key">Access Key ID</label>
      <input id="aws-access-key" v-model="credentials.accessKeyId" type="text" required />

      <label for="aws-secret-key">Secret Access Key</label>
      <input id="aws-secret-key" v-model="credentials.secretAccessKey" type="password" required />
    </div>

    <!-- GCP fields -->
    <div v-if="provider === 'gcp'" class="provider-fields">
      <label for="gcp-json">Service Account JSON</label>
      <textarea id="gcp-json" v-model="credentials.serviceAccountJson" rows="6" required></textarea>
    </div>

    <!-- Azure fields -->
    <div v-if="provider === 'azure'" class="provider-fields">
      <label for="azure-client-id">Client ID</label>
      <input id="azure-client-id" v-model="credentials.clientId" type="text" required />

      <label for="azure-tenant-id">Tenant ID</label>
      <input id="azure-tenant-id" v-model="credentials.tenantId" type="text" required />

      <label for="azure-client-secret">Client Secret</label>
      <input id="azure-client-secret" v-model="credentials.clientSecret" type="password" required />
    </div>

    <div class="actions">
      <button type="submit" :disabled="!isValid">Save Credentials</button>
    </div>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </form>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'

const emit = defineEmits(['credential-added'])

const provider = ref('')
const errorMessage = ref('')

const credentials = reactive({
  // AWS
  accessKeyId: '',
  secretAccessKey: '',
  // GCP
  serviceAccountJson: '',
  // Azure
  clientId: '',
  tenantId: '',
  clientSecret: '',
})

// Reset credential fields when provider changes
watch(provider, () => {
  // clear all fields
  credentials.accessKeyId = ''
  credentials.secretAccessKey = ''
  credentials.serviceAccountJson = ''
  credentials.clientId = ''
  credentials.tenantId = ''
  credentials.clientSecret = ''
  errorMessage.value = ''
})

// Simple validation per provider
const isValid = computed(() => {
  if (!provider.value) return false
  switch (provider.value) {
    case 'aws':
      return credentials.accessKeyId.trim() !== '' && credentials.secretAccessKey.trim() !== ''
    case 'gcp':
      return credentials.serviceAccountJson.trim() !== ''
    case 'azure':
      return (
        credentials.clientId.trim() !== '' &&
        credentials.tenantId.trim() !== '' &&
        credentials.clientSecret.trim() !== ''
      )
    default:
      return false
  }
})

function handleSubmit() {
  if (!isValid.value) {
    errorMessage.value = 'Please fill in all required fields.'
    return
  }

  // Prepare payload based on provider
  let payload = { provider: provider.value }

  switch (provider.value) {
    case 'aws':
      payload = {
        ...payload,
        accessKeyId: credentials.accessKeyId.trim(),
        secretAccessKey: credentials.secretAccessKey.trim(),
      }
      break
    case 'gcp':
      payload = {
        ...payload,
        serviceAccountJson: credentials.serviceAccountJson.trim(),
      }
      break
    case 'azure':
      payload = {
        ...payload,
        clientId: credentials.clientId.trim(),
        tenantId: credentials.tenantId.trim(),
        clientSecret: credentials.clientSecret.trim(),
      }
      break
  }

  // Emit to parent for further processing (validation against cloud APIs, saving, etc.)
  emit('credential-added', payload)

  // Reset form
  provider.value = ''
}
</script>

<style scoped>
.provider-setup-form {
  max-width: 500px;
  margin: 1rem auto;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #fafafa;
}
.provider-setup-form h2 {
  margin-bottom: 1rem;
}
.provider-setup-form label {
  display: block;
  margin-top: 0.75rem;
  font-weight: 600;
}
.provider-setup-form input,
.provider-setup-form select,
.provider-setup-form textarea {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.25rem;
  box-sizing: border-box;
}
.actions {
  margin-top: 1.5rem;
  text-align: right;
}
.actions button {
  padding: 0.5rem 1rem;
}
.error {
  color: #c00;
  margin-top: 0.5rem;
}
</style>