from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

import stripe
from django.conf import settings
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from cart.models import Cart
from orders.models import Order, OrderItem

User = get_user_model()

class CreateCheckoutSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        if not settings.STRIPE_SECRET_KEY:
            return Response(
                {"detail": "Stripe is not configured (missing STRIPE_SECRET_KEY)."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        cart, _ = Cart.objects.select_related("user").prefetch_related("items__product").get_or_create(
            user=request.user
        )
        items = list(cart.items.all())
        if not items:
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        currencies = {item.product.currency for item in items}
        if len(currencies) != 1:
            return Response(
                {"detail": "All cart items must use the same currency."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        currency = currencies.pop()

        total = Decimal("0.00")
        order = Order.objects.create(user=request.user, status=Order.Status.PENDING, currency=currency)

        line_items = []
        for item in items:
            product = item.product
            unit_price = product.price
            line_total = (unit_price * item.quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total += line_total

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                unit_price=unit_price,
                quantity=item.quantity,
                line_total=line_total,
            )

            unit_amount = int((unit_price * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
            line_items.append(
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {"name": product.name},
                        "unit_amount": unit_amount,
                    },
                    "quantity": item.quantity,
                }
            )

        order.total_amount = total
        order.save(update_fields=["total_amount"])

        stripe.api_key = settings.STRIPE_SECRET_KEY

        success_url = f"{settings.FRONTEND_URL}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{settings.FRONTEND_URL}/checkout/cancel"

        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=str(order.id),
            metadata={
                "order_id": str(order.id),
                "user_id": str(request.user.id),
            },
        )

        order.stripe_checkout_session_id = session.id
        order.save(update_fields=["stripe_checkout_session_id"])

        return Response({"checkout_url": session.url, "order_id": order.id})


def _mark_order_paid_and_after(session_id: str) -> bool:
    """Met à jour la commande en paid, vide le panier et envoie l'email. Idempotent."""
    updated = Order.objects.filter(stripe_checkout_session_id=session_id).update(status=Order.Status.PAID)
    if not updated:
        return False
    order = Order.objects.filter(stripe_checkout_session_id=session_id).first()
    if not order:
        return True
    user_id = order.user_id
    try:
        Cart.objects.get(user_id=user_id).items.all().delete()
    except Cart.DoesNotExist:
        pass
    try:
        user = User.objects.get(id=user_id)
        if user.email:
            send_mail(
                subject="Confirmation de votre commande ! ",
                message=f"Bonjour {user.username},\n\nVotre paiement a bien été reçu. Nous préparons votre commande avec amour !\n\nMerci de votre confiance et à très vite sur notre boutique.",
                from_email="contact@maboutique.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
    except User.DoesNotExist:
        pass
    return True


class ConfirmCheckoutSessionView(APIView):
    """Appelé depuis la page de succès avec le session_id : vérifie Stripe et passe la commande en paid si besoin."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        session_id = (request.query_params.get("session_id") or "").strip()
        if not session_id:
            return Response({"detail": "session_id required."}, status=status.HTTP_400_BAD_REQUEST)
        if not settings.STRIPE_SECRET_KEY:
            return Response({"detail": "Stripe not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.error.InvalidRequestError:
            return Response({"detail": "Invalid session_id."}, status=status.HTTP_400_BAD_REQUEST)
        if session.get("payment_status") != "paid":
            return Response({"detail": "Payment not completed."}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(stripe_checkout_session_id=session_id).first()
        if not order:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        if order.user_id != request.user.id:
            return Response({"detail": "Not your order."}, status=status.HTTP_403_FORBIDDEN)
        if order.status == Order.Status.PAID:
            return Response({"status": "already_paid", "order_id": order.id})
        _mark_order_paid_and_after(session_id)
        return Response({"status": "paid", "order_id": order.id})


@csrf_exempt
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse(status=500)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id", "")
        if session_id:
            _mark_order_paid_and_after(session_id)

    return HttpResponse(status=200)