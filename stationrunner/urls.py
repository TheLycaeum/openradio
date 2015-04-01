from django.conf.urls import patterns, url

from stationrunner.views import StationCreate
from stationrunner.views import StationView
from stationrunner.views import StationEdit
from stationrunner.views import ListStations
#from stationrunner.views import ChannelCreate
#from stationrunner.views import ChannelEdit
#from stationrunner.views import ChannelManage

urlpatterns = patterns('',
    url(r'^create_station/', StationCreate.as_view(), name='createstation'),
    url(r'^view_station/(?P<pk>\d+)/', StationView.as_view(), name='viewstation'),
    url(r'^edit_station/(?P<id>[\w-]+)/', StationEdit.as_view(), name='editstation'),
    url(r'^list_stations/', ListStations.as_view(), name='liststations'),    
#    url(r'^(?P<fk>\d+)/create_channel/', ChannelCreate.as_view(), name='createchannel'),
#    url(r'^(?P<fk>\d+)/edit_channel/(?P<id>[\w-]+)/', ChannelEdit.as_view(), name='editchannel'),
#    url(r'^(?P<fk>\d+)/manage_channel/(?P<id>[\w-]+)/', ChannelManage.as_view(), name='managechannel'),
                       
)
