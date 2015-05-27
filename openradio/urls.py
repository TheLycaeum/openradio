from django.conf.urls import patterns, include, url
from django.contrib import admin
from stationrunner import views
from stationrunner.views import UserRegistration
from stationrunner.views import UserHome
from stationrunner.views import Stations
from stationrunner.views import StationHome
from stationrunner.views import StationDelete
from stationrunner.views import Members
from stationrunner.views import MemberRemove
#from stationrunner.views import ChannelListCreate
#To Alen, channel related views import here
from stationrunner.views import Channels
from stationrunner.views import AudioFiles
from stationrunner.views import AudioFileHome
from stationrunner.views import Tags
from stationrunner.views import TagAdd
from stationrunner.views import TagRemove

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
    url(r'^user/(?P<pk>\d+)$', UserHome.as_view(), name='userhome'),
    url(r'^stations$', Stations.as_view(), name='stations'),
    url(r'^station/(?P<pk>\d+)$', StationHome.as_view(), name='home_station'),
    url(r'^station/(?P<pk>\d+)/delete$', StationDelete.as_view(), name='delete_station'),
    url(r'^station/(?P<pk>\d+)/members$', Members.as_view(), name='members'),
    url(r'^station/(?P<pk>\d+)/member/remove$', MemberRemove.as_view(), name='remove_member'),
    #url(r'^channels$', ChannelListCreate.as_view(), name='list_create_channel'),
    ##To Alen, all channel related urls here
    url(r'^channels$', Channels.as_view(), name='channels'),
    #url(r'^channelcreate$', channelcreate.as_view(), name='create_channels'),

    ##########                   
    url(r'^audio_files$', AudioFiles.as_view(), name='audio_files'),       
    url(r'^audio_file/(?P<pk>\d+)$', AudioFileHome.as_view(), name='home_audio'),
    url(r'^audio_file/(?P<pk>\d+)/tags$', Tags.as_view(), name='tags'),
    url(r'^audio_file/(?P<pk>\d+)/tag/add$', TagAdd.as_view(), name='add_tag'),
    url(r'^audio_file/(?P<pk>\d+)/tag/remove$', TagRemove.as_view(), name='remove_tag'),
)
