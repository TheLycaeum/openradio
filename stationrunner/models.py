from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Station(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(default='')
    owner = models.ForeignKey(User,default='')
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

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        
    def to_python(self, value):
        if not value:
            value = []
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
    
class AudioFile(models.Model):
    name = models.CharField(max_length=100)
    audio_file = models.FileField()
    tags = ListField()
    uploader = models.ForeignKey(User,default='')

    def __unicode__(self):
        return self.name        

class Playlist(models.Model):
    pass

class Channel(models.Model):
    name = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    owner = models.ForeignKey(User,default='')
    station = models.ForeignKey(Station,default='')
    playlists = models.ManyToManyField(Playlist)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("viewchannel", kwargs={"pk": self.pk})



