import React from 'react';
import { observer } from 'mobx-react-lite';
import { alertStore } from '../stores/alertStore';

const AlertSettings = observer(() => {
  // 1️⃣  Handlers that update the store directly
  const handleThresholdChange = (e) => {
    alertStore.setThreshold(e.target.value);
  };

  const handleEmailChange = (e) => {
    alertStore.setEmail(e.target.value);
  };

  const handleWebhookChange = (e) => {
    alertStore.setSlackWebhook(e.target.value);
  };

  return (
    <div style={{ maxWidth: 400, margin: '1rem auto', fontFamily: 'sans-serif' }}>
      <h2>Alert Settings</h2>

      <div style={{ marginBottom: 12 }}>
        <label>
          Spending Threshold ($):
          <input
            type="number"
            value={alertStore.threshold}
            onChange={handleThresholdChange}
            style={{ width: '100%' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: 12 }}>
        <label>
          Email Address:
          <input
            type="email"
            value={alertStore.email}
            onChange={handleEmailChange}
            style={{ width: '100%' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: 12 }}>
        <label>
          Slack Webhook URL:
          <input
            type="text"
            value={alertStore.slackWebhook}
            onChange={handleWebhookChange}
            style={{ width: '100%' }}
          />
        </label>
      </div>

      <button
        onClick={() => alert('Alert configuration saved.')}
        style={{ marginTop: 8 }}
      >
        Save Settings
      </button>
    </div>
  );
});

export default AlertSettings;