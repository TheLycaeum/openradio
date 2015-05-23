from django.conf.urls import patterns, include, url
from django.contrib import admin
from stationrunner.views import UserRegistration
from stationrunner.views import UserHome
from stationrunner.views import StationListCreate
from stationrunner.views import StationActualCreate
from stationrunner.views import StationHome
from stationrunner.views import MemberAdd
from stationrunner.views import MemberRemove
from stationrunner.views import StationEdit
from stationrunner.views import StationDelete
#from stationrunner.views import ChannelListCreate
#To Alen, channel related views import here
from stationrunner.views import Channels

from stationrunner.views import AudioFileListUpload
from stationrunner.views import AudioActualUpload
from stationrunner.views import AudioFileHome
from stationrunner import views

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
    url(r'^stations$', StationListCreate.as_view(), name='list_create_station'),
    url(r'^createstation$', StationActualCreate.as_view(), name='actual_create_station'),
    url(r'^station/(?P<pk>\d+)$', StationHome.as_view(), name='home_station'),
    url(r'^station/(?P<pk>\d+)/addmember$', MemberAdd.as_view(), name='add_member'),
    url(r'^station/(?P<pk>\d+)/removemember$', MemberRemove.as_view(), name='remove_member'),
    url(r'^station/(?P<pk>\d+)/editstation$', StationEdit.as_view(), name='edit_station'),
    url(r'^station/(?P<pk>\d+)/deletestation$', StationDelete.as_view(), name='delete_station'),
    #url(r'^channels$', ChannelListCreate.as_view(), name='list_create_channel'),
    ##To Alen, all channel related urls here
    url(r'^channels$', Channels.as_view(), name='channels'),
    #url(r'^channelcreate$', channelcreate.as_view(), name='create_channels'),

    ##########                   
    url(r'^audio_files$', AudioFileListUpload.as_view(), name='list_upload_audio_file'),       
    url(r'^uploadaudio$', AudioActualUpload.as_view(), name='actual_upload_audio'),
    url(r'^audio_files/(?P<pk>\d+)$', AudioFileHome.as_view(), name='home_audio'),
)
