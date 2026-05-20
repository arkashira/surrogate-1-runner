import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Onboarding: React.FC = () => {
  const [webhookUrl, setWebhookUrl] = useState<string>('');
  const [alertmanagerConfig, setAlertmanagerConfig] = useState<string>('');
  const [connectionStatus, setConnectionStatus] = useState<'green' | 'red' | 'unknown'>('unknown');
  const [testAlertSent, setTestAlertSent] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data: webhookData, data: alertmanagerData } = await axios.get('/api/webhook-url-and-config');
        setWebhookUrl(webhookData.webhookUrl);
        setAlertmanagerConfig(alertmanagerData.alertmanagerConfig);
        setConnectionStatus('unknown');
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
  }, []);

  const handleTestAlert = async () => {
    try {
      await axios.post('/api/test-alert');
      setTestAlertSent(true);
      setConnectionStatus('green');
    } catch (error) {
      console.error(error);
      setConnectionStatus('red');
    }
  };

  return (
    <div>
      <h1>Onboarding Setup</h1>
      <p>Webhook URL: {webhookUrl}</p>
      <p>Alertmanager Config:</p>
      <pre>{alertmanagerConfig}</pre>
      <button onClick={handleTestAlert}>Send Test Alert</button>
      {testAlertSent && (
        <p>
          Connection Status: <span style={{ color: connectionStatus === 'green' ? 'green' : 'red' }}>{connectionStatus}</span>
        </p>
      )}
    </div>
  );
};

export default Onboarding;