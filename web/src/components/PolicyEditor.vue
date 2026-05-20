<template>
  <div class="policy-editor">
    <h2>CAROL Policy Editor</h2>

    <draggable v-model="policy.conditions" handle=".drag-handle" class="conditions-list">
      <transition-group name="list" tag="div">
        <div v-for="(cond, index) in policy.conditions" :key="cond.id" class="condition-item">
          <span class="drag-handle">☰</span>

          <select v-model="cond.type" @change="clearError(index)">
            <option disabled value="">Select condition type</option>
            <option v-for="type in conditionTypes" :key="type" :value="type">{{ type }}</option>
          </select>

          <input
            type="text"
            v-model="cond.value"
            placeholder="Enter value"
            @input="clearError(index)"
          />

          <button @click="removeCondition(index)" class="remove-btn">✕</button>

          <div v-if="validationErrors[index]" class="error-msg">
            {{ validationErrors[index] }}
          </div>
        </div>
      </transition-group>
    </draggable>

    <button @click="addCondition" class="add-btn">Add Condition</button>

    <div class="save-section">
      <button @click="savePolicy" class="save-btn">Save Policy</button>
      <div v-if="saveError" class="save-error">{{ saveError }}</div>
      <div v-if="saveSuccess" class="save-success">Policy saved (version {{ policy.version }})</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import draggable from 'vuedraggable';

// Unique ID generator for list keys
let nextId = 1;

// Define the shape of a condition
interface Condition {
  id: number;
  type: string;
  value: string;
}

// Reactive policy object
const policy = reactive({
  version: 1,
  conditions: [] as Condition[],
});

// Available condition types (can be expanded later)
const conditionTypes = [
  'Dataset Provenance',
  'Model Size',
];

// Validation errors per condition index
const validationErrors = ref<Record<number, string>>({});

// Global save status messages
const saveError = ref('');
const saveSuccess = ref(false);

// Add a new empty condition
function addCondition() {
  policy.conditions.push({
    id: nextId++,
    type: '',
    value: '',
  });
}

// Remove condition at index
function removeCondition(index: number) {
  policy.conditions.splice(index, 1);
  // Clean up any existing error for that index
  delete validationErrors.value[index];
}

// Clear error for a specific condition when user edits it
function clearError(index: number) {
  delete validationErrors.value[index];
}

// Simple validation: each condition must have a type and a non‑empty value
function validatePolicy(): boolean {
  let valid = true;
  validationErrors.value = {};

  policy.conditions.forEach((cond, idx) => {
    if (!cond.type) {
      validationErrors.value[idx] = 'Condition type is required.';
      valid = false;
    } else if (!cond.value.trim()) {
      validationErrors.value[idx] = 'Condition value cannot be empty.';
      valid = false;
    }
  });

  return valid;
}

// Persist policy to backend (PostgreSQL via API)
async function savePolicy() {
  saveError.value = '';
  saveSuccess.value = false;

  if (!validatePolicy()) {
    saveError.value = 'Please fix validation errors before saving.';
    return;
  }

  // Prepare payload with versioning
  const payload = {
    version: policy.version,
    conditions: policy.conditions.map(({ type, value }) => ({ type, value })),
  };

  try {
    const response = await fetch('/api/policies', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Server responded ${response.status}: ${errText}`);
    }

    // Increment version after successful save
    policy.version += 1;
    saveSuccess.value = true;
  } catch (e: any) {
    saveError.value = `Failed to save policy: ${e.message}`;
  }
}
</script>

<style scoped>
.policy-editor {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
  font-family: Arial, sans-serif;
}

.conditions-list {
  margin-bottom: 1rem;
}

.condition-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  background: #fafafa;
}

.drag-handle {
  cursor: grab;
  user-select: none;
}

.remove-btn {
  background: transparent;
  border: none;
  color: #c00;
  font-size: 1.2rem;
  cursor: pointer;
}

.add-btn,
.save-btn {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: #2d8cf0;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-btn:hover,
.save-btn:hover {
  background: #1a73e8;
}

.error-msg {
  color: #c00;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.save-error {
  color: #c00;
  margin-top: 0.5rem;
}

.save-success {
  color: #090;
  margin-top: 0.5rem;
}
</style>