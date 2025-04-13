from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['name', 'description', 'price', 'latitude', 'longitude']
    


