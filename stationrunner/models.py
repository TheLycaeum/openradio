from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Station(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    owner = models.ForeignKey(User)
    members = models.ManyToManyField(User,related_name='members')

    def __unicode__(self):
        return self.name
        
#   To team members, methods add_member, remove_member and 
#   check_membership are not required as adding to a Django 
#   ManyToMany field is as simple as 
#   "<object_name>.members.add(<object_name>)" and to remove, 
#   "<object_name>.members.remove(<object_name>)".
#   Finally, to check membership of a user we can simply do
#   "assert <object_name> in <object_name>.members.all()"

class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class AudioFile(models.Model):
    name = models.CharField(max_length=100)
    audio_file = models.FileField()
    tags = models.ManyToManyField(Tag)
    uploader = models.ForeignKey(User)

    def __unicode__(self):
        return self.name        

class Playlist(models.Model):
    pass

class Channel(models.Model):
    name = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    station = models.ForeignKey(Station)
    playlists = models.ManyToManyField(Playlist)

    def __unicode__(self):
        return self.name
