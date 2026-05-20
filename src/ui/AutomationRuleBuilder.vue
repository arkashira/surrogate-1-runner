<template>
  <div class="automation-rule-builder">
    <h2>Create Automation Rule</h2>

    <div class="field">
      <label for="rule-name">Rule Name</label>
      <input id="rule-name" v-model="rule.name" placeholder="Enter rule name" />
    </div>

    <div class="field">
      <label for="trigger-select">Trigger</label>
      <select id="trigger-select" v-model="rule.trigger">
        <option disabled value="">Select a trigger</option>
        <option v-for="t in triggers" :key="t.value" :value="t.value">
          {{ t.label }}
        </option>
      </select>
    </div>

    <div class="field">
      <label for="actions-select">Actions</label>
      <select id="actions-select" v-model="selectedAction" @change="addAction">
        <option disabled value="">Add an action</option>
        <option v-for="a in availableActions" :key="a.value" :value="a.value">
          {{ a.label }}
        </option>
      </select>
    </div>

    <div class="actions-list" v-if="rule.actions.length">
      <h3>Configured Actions</h3>
      <ul>
        <li v-for="(action, idx) in rule.actions" :key="idx">
          <strong>{{ actionLabel(action.type) }}</strong>
          <div v-if="action.type === 'assign_user'">
            <label>User:</label>
            <input v-model="action.payload.user" placeholder="GitHub username" />
          </div>
          <div v-else-if="action.type === 'send_slack'">
            <label>Channel:</label>
            <input v-model="action.payload.channel" placeholder="#general" />
            <label>Message:</label>
            <input v-model="action.payload.message" placeholder="Message text" />
          </div>
          <div v-else-if="action.type === 'create_jira'">
            <label>Project Key:</label>
            <input v-model="action.payload.projectKey" placeholder="PROJ" />
            <label>Summary:</label>
            <input v-model="action.payload.summary" placeholder="Issue summary" />
          </div>
          <button @click="removeAction(idx)" class="remove-btn">Remove</button>
        </li>
      </ul>
    </div>

    <div class="field toggle-enabled">
      <label>
        <input type="checkbox" v-model="rule.enabled" />
        Enabled
      </label>
    </div>

    <div class="buttons">
      <button @click="showPreview = true" :disabled="!canSave">Preview</button>
      <button @click="saveRule" :disabled="!canSave">Save Rule</button>
    </div>

    <RulePreview
      v-if="showPreview"
      :rule="rule"
      @close="showPreview = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import axios from 'axios';
import RulePreview from './RulePreview.vue';

interface ActionConfig {
  type: string;
  payload: Record<string, any>;
}

interface AutomationRule {
  name: string;
  enabled: boolean;
  trigger: string;
  actions: ActionConfig[];
}

const rule = ref<AutomationRule>({
  name: '',
  enabled: true,
  trigger: '',
  actions: [],
});

const triggers = [
  { value: 'github_issue', label: 'GitHub Issue Event' },
  { value: 'jira_update', label: 'Jira Update' },
];

const availableActions = [
  { value: 'assign_user', label: 'Assign User' },
  { value: 'send_slack', label: 'Send Slack Message' },
  { value: 'create_jira', label: 'Create Jira Issue' },
];

const selectedAction = ref<string>('');

function addAction() {
  if (!selectedAction.value) return;
  // Prevent duplicate action types for simplicity
  if (rule.value.actions.some(a => a.type === selectedAction.value)) {
    selectedAction.value = '';
    return;
  }

  const newAction: ActionConfig = {
    type: selectedAction.value,
    payload: {},
  };
  // Initialize payload fields for UI convenience
  switch (newAction.type) {
    case 'assign_user':
      newAction.payload = { user: '' };
      break;
    case 'send_slack':
      newAction.payload = { channel: '', message: '' };
      break;
    case 'create_jira':
      newAction.payload = { projectKey: '', summary: '' };
      break;
  }
  rule.value.actions.push(newAction);
  selectedAction.value = '';
}

function removeAction(idx: number) {
  rule.value.actions.splice(idx, 1);
}

function actionLabel(type: string): string {
  const found = availableActions.find(a => a.value === type);
  return found ? found.label : type;
}

const canSave = computed(() => {
  return rule.value.name && rule.value.trigger && rule.value.actions.length > 0;
});

async function saveRule() {
  try {
    await axios.post('/api/rules', rule.value);
    alert('Rule saved successfully');
    // Reset form
    rule.value = {
      name: '',
      enabled: true,
      trigger: '',
      actions: [],
    };
  } catch (e) {
    console.error(e);
    alert('Failed to save rule');
  }
}

const showPreview = ref(false);
</script>

<style scoped>
.automation-rule-builder {
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.field {
  margin-bottom: 1rem;
}
.field label {
  display: block;
  margin-bottom: 0.3rem;
}
.field input,
.field select {
  width: 100%;
  padding: 0.4rem;
  box-sizing: border-box;
}
.actions-list ul {
  list-style: none;
  padding: 0;
}
.actions-list li {
  background: #f9f9f9;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
}
.remove-btn {
  margin-top: 0.5rem;
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.3rem 0.6rem;
  cursor: pointer;
}
.toggle-enabled {
  display: flex;
  align-items: center;
}
.buttons {
  display: flex;
  gap: 0.5rem;
}
.buttons button {
  flex: 1;
  padding: 0.5rem;
}
</style>