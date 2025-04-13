from rest_framework import serializers
from .models import Produit

class ProduitSerializer(serializers.ModelSerializer):
    # permet de serialiser un model créé
    class Meta:
        model = Produit
        fields = ('name', 'description', 'price', 'latitude', 'longitude')