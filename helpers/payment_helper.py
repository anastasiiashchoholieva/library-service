import stripe
from decimal import Decimal
from django.conf import settings
from django.urls import reverse

from payments.models import Payment


def create_stripe_session(borrowing, request):
    book = borrowing.book
    daily_fee = book.daily_fee
    borrow_date = borrowing.borrow_date
    expected_return_date = borrowing.expected_return_date

    borrowed_days = (expected_return_date - borrow_date).days
    total_price = daily_fee * borrowed_days
    unit_amount = int(total_price * 100)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    success_url = request.build_absolute_uri(reverse("payments:payment-success", kwargs={"session_id": "<session_id>"}))
    cancel_url = request.build_absolute_uri(reverse("payments:payment-cancel", kwargs={"session_id": "<session_id>"}))

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": unit_amount,
                "product_data": {
                    "name": borrowing.book.title,
                },
            },
            "quantity": 1,
        }],
        metadata={
            "product_id": borrowing.id
        },
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )

    payment = Payment.objects.create(
        status=Payment.PaymentStatus.PENDING,
        type=Payment.PaymentType.PAYMENT,
        borrowing_id=borrowing.id,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=Decimal(total_price),
    )

    return payment
