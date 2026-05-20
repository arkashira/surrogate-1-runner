<template>
  <div class="upload-pricing">
    <h2>Upload Competitor Pricing</h2>
    <form @submit.prevent="handleSubmit" enctype="multipart/form-data">
      <div class="form-group">
        <label for="csvFile">CSV File (max 5 MB)</label>
        <input
          type="file"
          id="csvFile"
          accept=".csv"
          @change="onFileChange"
          required
        />
      </div>
      <button type="submit" :disabled="!file || uploading">
        {{ uploading ? 'Uploading...' : 'Upload' }}
      </button>
    </form>

    <div v-if="error" class="alert alert-danger mt-3">
      {{ error }}
    </div>

    <div v-if="success" class="alert alert-success mt-3">
      Upload accepted! Your data is being processed.
    </div>

    <div v-if="validationErrors.length" class="mt-3">
      <h4>Validation Errors:</h4>
      <ul>
        <li v-for="(err, idx) in validationErrors" :key="idx">
          {{ err }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'UploadPricing',
  setup() {
    const file = ref<File | null>(null);
    const uploading = ref(false);
    const error = ref<string | null>(null);
    const success = ref(false);
    const validationErrors = ref<string[]>([]);

    const onFileChange = (e: Event) => {
      const target = e.target as HTMLInputElement;
      if (target.files && target.files[0]) {
        const selectedFile = target.files[0];
        if (selectedFile.size > 5 * 1024 * 1024) {
          error.value = 'File size exceeds 5 MB limit.';
          file.value = null;
        } else {
          error.value = null;
          file.value = selectedFile;
        }
      }
    };

    const handleSubmit = async () => {
      if (!file.value) return;
      uploading.value = true;
      error.value = null;
      success.value = false;
      validationErrors.value = [];

      const formData = new FormData();
      formData.append('file', file.value);

      try {
        const response = await axios.post('/api/competitor-price/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          validateStatus: (status) => status < 500, // handle 400/202
        });

        if (response.status === 202) {
          success.value = true;
        } else if (response.status === 400) {
          error.value = response.data.message || 'Bad request.';
        } else {
          error.value = 'Unexpected response from server.';
        }

        if (response.data && response.data.validationErrors) {
          validationErrors.value = response.data.validationErrors;
        }
      } catch (err: any) {
        error.value = err.response?.data?.message || 'Network error.';
      } finally {
        uploading.value = false;
      }
    };

    return {
      file,
      uploading,
      error,
      success,
      validationErrors,
      onFileChange,
      handleSubmit,
    };
  },
});
</script>

<style scoped>
.upload-pricing {
  max-width: 600px;
  margin: 0 auto;
}
.form-group {
  margin-bottom: 1rem;
}
button {
  padding: 0.5rem 1rem;
}
.alert {
  padding: 0.75rem 1rem;
  border-radius: 0.25rem;
}
.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}
.alert-success {
  background-color: #d4edda;
  color: #155724;
}
</style>