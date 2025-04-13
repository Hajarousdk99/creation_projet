from django.urls import path
from . import views

urlpatterns = [
    path('produit/nouveau/', views.creer_produit, name='creer_produit'),]
