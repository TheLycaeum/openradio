from django.conf.urls import patterns, include, url
from django.contrib import admin
from stationrunner import views
from stationrunner.views import UserRegistration
from stationrunner.views import UserHome
from stationrunner.views import StationListCreate
from stationrunner.views import StationHome
from stationrunner.views import StationEdit
from stationrunner.views import ChannelCreate
from stationrunner.views import ChannelHome
from stationrunner.views import ChannelEdit
from stationrunner.views import ListChannels
#from stationrunner.views import ChannelManage


urlpatterns = patterns('',
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 
        'django.contrib.auth.views.login', 
        {'template_name':'auth/login.html'
     }, 
        name='userlogin'
    ),
    url(r'^users$', UserRegistration.as_view( ), name='userregistration'),
    url(r'^user_redirect/', views.user_redirect, name='userredirect'),
    url(r'^users/(?P<pk>\d+)$', UserHome.as_view(), name='userhome'),
    #url(r'^(?P<username>\s+)/edit/', UserEdit.as_view(), name='useredit'),
    url(r'^stations$', StationListCreate.as_view(), name='list_create_station'),
    url(r'^stations/edit/(?P<pk>\d+)$', StationEdit.as_view(), name='editstation'),
    url(r'^stations/(?P<pk>\d+)$', StationHome.as_view(), name='viewstation'),
    url(r'^channels/new$', ChannelCreate.as_view(), name='createchannel'),
    url(r'^channels/edit/(?P<pk>\d+)$', ChannelEdit.as_view(), name='editchannel'),
    url(r'^channels/(?P<pk>\d+)$', ChannelHome.as_view(), name='viewchannel'),
    url(r'^channels$', ListChannels.as_view(), name = 'listchannels'),

)       
