import axios from 'axios';
import { Stripe } from '@stripe/stripe-js';

const stripe = new Stripe('YOUR_STRIPE_SECRET_KEY');

const createCheckoutSession = async (priceId: string) => {
  try {
    const response = await axios.post('/api/stripe/create-checkout-session', {
      priceId,
    });
    return response.data.checkoutSessionUrl;
  } catch (error) {
    console.error(error);
  }
};

export { createCheckoutSession };