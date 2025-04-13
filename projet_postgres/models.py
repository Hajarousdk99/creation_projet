from django.contrib.gis.db import models 
from django.contrib.postgres.search import SearchVectorField 

class Product(models.models): 
    name = models.CharField(max_length=255)
    price= models.FloatField() 
    ref= models.CharField(max_length=255, unique=True)
    description= models.TextField()
    latitude=models.FloatField
    longitude= models.FloatField() 
    geolocalisation= models.PointField(srid=4236,geography=True)
    name_desc = SearchVectorField(verbose_name=["name","description"])
    class Meta: 
        indexes= [models.Index(fields=["name_desc"])]
         