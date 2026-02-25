from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from catalog.models import Product

from .models import Cart, CartItem
from .serializers import CartItemAddSerializer, CartItemSerializer, CartSerializer


def _get_or_create_cart(user) -> Cart:
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return _get_or_create_cart(self.request.user)


class CartItemAddView(generics.GenericAPIView):
    serializer_class = CartItemAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = _get_or_create_cart(request.user)
        product = get_object_or_404(Product, pk=serializer.validated_data["product_id"], is_active=True)
        quantity = serializer.validated_data["quantity"]

        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])

        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemUpdateDeleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = _get_or_create_cart(self.request.user)
        return CartItem.objects.filter(cart=cart).select_related("product")

    def patch(self, request, pk: int, *args, **kwargs):
        item = get_object_or_404(self.get_queryset(), pk=pk)
        quantity = request.data.get("quantity")
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response({"quantity": "Must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        if quantity < 1:
            return Response({"quantity": "Must be >= 1."}, status=status.HTTP_400_BAD_REQUEST)
        item.quantity = quantity
        item.save(update_fields=["quantity"])
        return Response(CartItemSerializer(item).data)

    def delete(self, request, pk: int, *args, **kwargs):
        item = get_object_or_404(self.get_queryset(), pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
