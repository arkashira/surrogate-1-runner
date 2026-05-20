import axios from 'axios';

const getWebhookUrlAndConfig = async () => {
  try {
    const response = await axios.get('/api/webhook-url');
    return {
      webhookUrl: response.data.webhookUrl,
      alertmanagerConfig: response.data.alertmanagerConfig
    };
  } catch (error) {
    console.error(error);
  }
};

export { getWebhookUrlAndConfig };