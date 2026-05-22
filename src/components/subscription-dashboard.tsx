import React from 'react';
import { useStripe } from '@stripe/react-stripe-js';
import { useSubscription } from './use-subscription';

const SubscriptionDashboard = () => {
  const stripe = useStripe();
  const { subscription, error } = useSubscription();

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!subscription) {
    return <div>Please subscribe to access LLM gateway features</div>;
  }

  return (
    <div>
      <h2>Pricing Tiers and Features</h2>
      <ul>
        <li>Basic: $9.99/month (limited features)</li>
        <li>Pro: $29.99/month (full features)</li>
      </ul>
      <h2>Subscription Status</h2>
      <p>Subscription ID: {subscription.id}</p>
      <p>Next billing cycle: {subscription.current_period_end}</p>
    </div>
  );
};

export default SubscriptionDashboard;