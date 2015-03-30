from django.conf.urls import patterns, url

from stationrunner.views import StationCreate

urlpatterns = patterns('',
    url(r'^stations/create/', StationCreate.as_view(), name='createstation'),
                       
)
