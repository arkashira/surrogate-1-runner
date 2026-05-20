import React, { useState } from 'react';
import './AlertConfigForm.css';

const AlertConfigForm = () => {
  const [threshold, setThreshold] = useState('');
  const [email, setEmail] = useState('');
  const [slackWebhook, setSlackWebhook] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // Logic to save the alert configuration
    console.log('Threshold:', threshold);
    console.log('Email:', email);
    console.log('Slack Webhook:', slackWebhook);
  };

  return (
    <form onSubmit={handleSubmit} className="alert-config-form">
      <label>
        Alert Threshold:
        <input type="number" value={threshold} onChange={(e) => setThreshold(e.target.value)} />
      </label>
      <label>
        Email Notification:
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </label>
      <label>
        Slack Webhook URL:
        <input type="text" value={slackWebhook} onChange={(e) => setSlackWebhook(e.target.value)} />
      </label>
      <button type="submit">Save Configuration</button>
    </form>
  );
};

export default AlertConfigForm;