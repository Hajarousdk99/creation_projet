from rest_framework import generics, permissions

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Category.objects.all()
        parent_slug = self.request.query_params.get("parent")
        if parent_slug is not None:
            if parent_slug == "":
                qs = qs.filter(parent__isnull=True)
            else:
                qs = qs.filter(parent__slug=parent_slug)
        else:
            qs = qs.filter(parent__isnull=True)
        return qs.order_by("name")


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related("category")
        category_slug = self.request.query_params.get("category")
        parent_slug = self.request.query_params.get("parent")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if parent_slug:
            qs = qs.filter(category__parent__slug=parent_slug)
        return qs


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
