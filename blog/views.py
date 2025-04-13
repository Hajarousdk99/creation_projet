from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, redirect
from .serializers import ProduitSerializer
from .models import Produit

@api_view(['POST'])
@csrf_exempt
def creer_produit(request: Request):
    if request.method == 'POST':
        try:
            serializer = ProduitSerializer(data=request.data)
            if serializer.is_valid():
                new_produit = Produit(
                    name=serializer.data.get('name'),
                    description=serializer.data.get('description'),
                    price=serializer.data.get('price'),
                    longitude=serializer.data.get('longitude'),
                    latitude=serializer.data.get('latitude'),
                )
                new_produit.save()
                return Response({
                    "message": "Enregsitrement ok"
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"message": "Erreur lors de la serialisation. Mauvaise donnée."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"message": f"Une erreur s'est produite: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(
            {"message": "Méthode non autorisé"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


