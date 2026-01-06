import stripe
import os
from dotenv import load_dotenv

load_dotenv()

# Stripe API Key set karein
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout_session(item_name, amount_pkr):
    try:
        # Stripe hamesha "Cents" ya sabse choti unit mein paise leta hai
        # Agar 500 PKR hai, toh humein 500 * 100 bhejna hoga
        unit_amount = int(amount_pkr * 100)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'pkr',
                    'product_data': {
                        'name': item_name,
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://example.com/success', # Payment hone ke baad yahan jayega
            cancel_url='https://example.com/cancel',   # Cancel karne par yahan
        )
        return session.url
    except Exception as e:
        return f"Stripe Error: {str(e)}"