from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Station(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(default='')
    owner = models.ForeignKey(User,default='')
    members = models.ManyToManyField(User, related_name='members')        
#   To team members, methods add_member, remove_member and 
#   check_membership are not required as adding to a Django 
#   ManyToMany field is as simple as 
#   "<object_name>.members.add(<object_name>)" and to remove, 
#   "<object_name>.members.remove(<object_name>)".
#   Finally, to check membership of a user we can simply do
#   "assert <object_name> in <object_name>.members.all()"
        
    def get_absolute_url(self):
        return reverse("viewstation", kwargs={"pk": self.pk})

class Playlist(models.Model):
    pass

class Channel(models.Model):
    name = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    owner = models.ForeignKey(User,default='')
    station = models.ForeignKey(Station,default='')
    playlists = models.ManyToManyField(Playlist)

    def get_absolute_url(self):
        return reverse("viewchannel", kwargs={"pk": self.pk})



