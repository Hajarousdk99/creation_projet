from django.urls import path

from .views import ConfirmCheckoutSessionView, CreateCheckoutSessionView, stripe_webhook

urlpatterns = [
    path("create-checkout-session/", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path("confirm-checkout-session/", ConfirmCheckoutSessionView.as_view(), name="confirm-checkout-session"),
    path("webhook/stripe/", stripe_webhook, name="stripe-webhook"),
]



