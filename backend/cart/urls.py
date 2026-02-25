from django.urls import path

from .views import CartDetailView, CartItemAddView, CartItemUpdateDeleteView

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart-detail"),
    path("items/", CartItemAddView.as_view(), name="cart-item-add"),
    path("items/<int:pk>/", CartItemUpdateDeleteView.as_view(), name="cart-item-update-delete"),
]

