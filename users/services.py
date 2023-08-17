
import os

import stripe
from rest_framework import serializers

from course.models import Course, Lesson
from users.models import Payment


def get_session_of_payment(
        self, success_url: str = 'https://example.com/success',
) -> stripe.checkout.Session:

    stripe.api_key = os.getenv('STRIPE_TOKEN')

    amount = self.request.data.get('amount')
    paid_lesson_id = self.request.data.get('paid_lesson')
    paid_course_id = self.request.data.get('paid_course')

    payment_obj = get_payment_obj(paid_lesson_id, paid_course_id)

    if payment_obj:
        stripe_product = get_product(payment_obj)

        stripe_price = get_price(amount, stripe_product)

        line_items = get_line_items(stripe_price)

    return stripe.checkout.Session.create(
        success_url=success_url,
        line_items=[
            line_items,
        ],
        mode='payment',
    )


def get_payment_obj(
        paid_lesson_id: int or None,
        paid_course_id: int or None,
) -> Course or Lesson or None:

    if paid_course_id:
        return Course.objects.get(pk=paid_course_id)

    if paid_lesson_id:
        return Lesson.objects.get(pk=paid_lesson_id)

    return None


def get_product(
        payment_obj: Course or Lesson,
) -> stripe.Product:

    return stripe.Product.create(name=payment_obj.name)


def get_price(
        amount: int,
        stripe_product: stripe.Product,
) -> stripe.Price:

    return stripe.Price.create(
        unit_amount=amount * 100,
        currency='rub',
        product=stripe_product.stripe_id,
    )


def get_line_items(
        stripe_price: stripe.Price,
        quantity: int = 1,
) -> dict:

    return {
        'price': stripe_price.stripe_id,
        'quantity': quantity,
    }


def save_serializer(
        self,
        session: stripe.checkout.Session,
        serializer: serializers,
) -> None:

    serializer.save(
        stripe_payment_id=session.get('id'),
        stripe_payment_url=session.get('url'),
        status=session.get('status'),
        user=self.request.user,
        method=Payment.TRANSFER,
    )
    

def get_stripe_data(payment: Payment):
    
    stripe.api_key = os.getenv('STRIPE_TOKEN')
    return stripe.checkout.Session.retrieve(
        payment.stripe_payment_id,
    )