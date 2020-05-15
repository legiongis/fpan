from django.contrib.gis.db import models

class Region(models.Model):
    name = models.CharField(max_length=254)
    region_code = models.CharField(max_length=4)
    geom = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.name
        