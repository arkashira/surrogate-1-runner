import { useState, useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { Subscription } from './billing';

const stripePromise = loadStripe('YOUR_STRIPE_PUBLISHABLE_KEY');

const useSubscription = () => {
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [error, setError] = useState<StripeError | null>(null);

  useEffect(() => {
    const fetchSubscription = async () => {
      try {
        const stripe = await stripePromise;
        const subscription = await stripe.retrieveSubscription('YOUR_STRIPE_SUBSCRIPTION_ID');
        setSubscription(subscription);
      } catch (error) {
        setError(error as StripeError);
      }
    };

    fetchSubscription();
  }, []);

  return { subscription, error };
};

export default useSubscription;