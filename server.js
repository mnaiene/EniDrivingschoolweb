// server.js

import express from 'express';
import Stripe from 'stripe';
import cors from 'cors';

const app = express();
const PORT = 4242;

// Your Stripe Secret Key (replace this with your own secret key)
const stripe = new Stripe('YOUR_STRIPE_SECRET_KEY', {
  apiVersion: '2022-11-15',
});

// Middlewares
app.use(cors());
app.use(express.json());

// Create Checkout Session
app.post('/create-checkout-session', async (req, res) => {
  const { uid } = req.body; // Optional: uid from Firebase user

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      line_items: [
        {
          price_data: {
            currency: 'eur',
            product_data: {
              name: 'Curso Online - ENI',
            },
            unit_amount: 5000, // 50 EUR = 5000 cents
          },
          quantity: 1,
        },
      ],
      success_url: 'http://localhost/escolacond/student-dashboard.html?success=true',
      cancel_url: 'http://localhost/escolacond/payment.html?canceled=true',
    });

    res.json({ id: session.id });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Stripe Server running at http://localhost:${PORT}`);
});

app.get('/', (req, res) => {
  res.send('Stripe server is running!');
});