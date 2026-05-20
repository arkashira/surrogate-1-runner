import axios from 'axios';
import { Stripe } from '@stripe/stripe-js';

const stripe = new Stripe('YOUR_STRIPE_SECRET_KEY');

const createCheckoutSession = async (req: any, res: any) => {
  try {
    const priceId = req.body.priceId;
    const checkoutSession = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      mode: 'subscription',
      success_url: 'https://example.com/success',
      cancel_url: 'https://example.com/cancel',
    });
    res.json({ checkoutSessionUrl: checkoutSession.url });
  } catch (error) {
    console.error(error);
  }
};

export default createCheckoutSession;