import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { StripeCheckout } from '@stripe/stripe-js';

const Subscription = () => {
  const [subscriptionStatus, setSubscriptionStatus] = useState(null);
  const [cancelLink, setCancelLink] = useState(null);

  useEffect(() => {
    const fetchSubscriptionStatus = async () => {
      try {
        const response = await axios.get('/api/subscription');
        setSubscriptionStatus(response.data.status);
        setCancelLink(response.data.cancelLink);
      } catch (error) {
        console.error(error);
      }
    };
    fetchSubscriptionStatus();
  }, []);

  const handleUpgrade = async () => {
    try {
      const response = await axios.post('/api/upgrade-subscription');
      window.location.href = response.data.checkoutSessionUrl;
    } catch (error) {
      console.error(error);
    }
  };

  const handleDowngrade = async () => {
    try {
      const response = await axios.post('/api/downgrade-subscription');
      window.location.href = response.data.checkoutSessionUrl;
    } catch (error) {
      console.error(error);
    }
  };

  const handleCancel = async () => {
    try {
      await axios.post('/api/cancel-subscription');
      setSubscriptionStatus('inactive');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Subscription Status: {subscriptionStatus}</h1>
      {cancelLink && (
        <button onClick={handleCancel}>
          Cancel Subscription
        </button>
      )}
      <button onClick={handleUpgrade}>
        Upgrade Subscription
      </button>
      <button onClick={handleDowngrade}>
        Downgrade Subscription
      </button>
    </div>
  );
};

export default Subscription;