import stripe
import os
from dotenv import load_dotenv

app = load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_subscription_session(customer_email: str, price_id: str):
    try:

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=customer_email,
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            success_url="https://your-domain.com/success",
            cancel_url="https://your-domain.com/cancel",
        )
        return session.url
    except Exception as e:
        return str(e)