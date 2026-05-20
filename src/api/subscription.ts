import axios from 'axios';

const getSubscriptionStatus = async () => {
  try {
    const response = await axios.get('/api/subscription');
    return response.data.status;
  } catch (error) {
    console.error(error);
  }
};

const upgradeSubscription = async () => {
  try {
    const response = await axios.post('/api/upgrade-subscription');
    return response.data.checkoutSessionUrl;
  } catch (error) {
    console.error(error);
  }
};

const downgradeSubscription = async () => {
  try {
    const response = await axios.post('/api/downgrade-subscription');
    return response.data.checkoutSessionUrl;
  } catch (error) {
    console.error(error);
  }
};

const cancelSubscription = async () => {
  try {
    await axios.post('/api/cancel-subscription');
  } catch (error) {
    console.error(error);
  }
};

export { getSubscriptionStatus, upgradeSubscription, downgradeSubscription, cancelSubscription };