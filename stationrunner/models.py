from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=50)
    
