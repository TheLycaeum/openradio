from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(default='')
    owner = models.ForeignKey('User',default='')
    
class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    email = models.EmailField()
