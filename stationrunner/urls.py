from django.conf.urls import patterns, url

from stationrunner.views import StationCreate
from stationrunner.views import StationView

urlpatterns = patterns('',
    url(r'^stations/create/', StationCreate.as_view(), name='createstation'),
    url(r'^stations/(?P<pk>\d+)/', StationView.as_view(), name='viewstation'),
                       
)
