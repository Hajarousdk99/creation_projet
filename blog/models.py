from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, LineString, Polygon, MultiPolygon
import uuid



class Produit(models.Model):
    name = models.CharField(max_length=200)
    reference = models.UUIDField()
    description = models.TextField()
    price = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    geolocalisation = models.PointField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = uuid.uuid4()
        if self.latitude and self.longitude:
            self.geolocalisation = Point(
                float(self.longitude),
                float(self.latitude),
                srid=4326
            )
            
        return super().save(*args, **kwargs)
      
    def _str_(self):
        return self.name
    
print(uuid.uuid4())


