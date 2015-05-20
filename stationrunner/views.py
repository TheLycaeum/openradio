from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.forms import Form
from django.views.generic import View
from django.views.generic.edit import CreateView
#from django.views.generic import DetailView
#from django.views.generic.edit import UpdateView
#from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Station, Channel, AudioFile
from .utils import handle_uploaded_file
from .forms import UserCreateForm, StationForm
from .forms import AddMemberForm, RemoveMemberForm
from .forms import AudioFileForm
from .utils import handle_uploaded_file

class UserRegistration(CreateView):
    template_name='auth/register.html'
    form_class=UserCreateForm

    def auth_login(self, request, username, password):
        '''
        Authenticate always needs to be called before login because it
        adds which backend did the authentication which is required by login.
        '''

        user = authenticate(username=username, password=password)
        login(request, user)

    def form_valid(self, form):
        '''
        Overwrite form_valid to login.
        '''

        #save the user
        response = super(UserRegistration, self).form_valid(form)

        #Get the user creditials
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        #authenticate and login
        self.auth_login(self.request, username, password)
        return response

@login_required
def user_redirect(request):
    url = reverse('userhome', kwargs={'pk':request.user.id})
    return HttpResponseRedirect(url)

class UserHome(View):
    def get(self, request, pk):
        rightful_user = User.objects.get(pk=pk)
        if request.user == rightful_user:
            return render(request, 
                          'home_user.html',
                          {'user':request.user,
                       }
            )
        else:
            return render(request, 'deny_user.html')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserHome, self).dispatch(*args, **kwargs)

class StationListCreate(View):
    def get(self, request):
        stations = Station.objects.filter(owner=request.user)
        return render(request,
                      'list_stations.html',
                      {'stations':stations},
        )

    def post(self, request):
        form = StationForm()
        return render(request, 'create_station.html', {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StationListCreate, self).dispatch(*args, **kwargs)

class StationActualCreate(View):
    def get(self, request):
        raise Http404

    def post(self, request):
        form = StationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            owner = request.user
            new_station_object = Station(name=name,
                                         address=address,
                                         owner=owner
            )
            new_station_object.save()
            return HttpResponseRedirect(reverse("home_station", 
                                                kwargs={'pk': new_station_object.id}
            ))
            
class StationHome(View):
    def get(self, request, pk):
        station = Station.objects.get(pk=pk)
        if station.owner == request.user:
            channels = Channel.objects.filter(station=station)
            members = station.members.all()
            form1 = AddMemberForm()
            form2 = RemoveMemberForm()
            form2.fields['member'].queryset = station.members.all()
            return render(request, 
                          "home_station.html",
                          {"station":station,
                           "form1":form1,
                           "form2":form2,
                           "channels":channels,
                           "members":members,
                       },
                      )
        else:
            return render(request,'deny_user.html')

    def post(self,request, pk):
        station = Station.objects.get(pk=pk)
        form = StationForm({'name': station.name,
                            'address': station.address,
                        }
                       )
        return render(request, 'edit_station.html', {'form':form,
                                                     'station':station
                                                 }
        )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StationHome, self).dispatch(*args, **kwargs)

class MemberAdd(View): 
    def get(self, request):
        raise Http404

    def post(self, request, pk):
        form = AddMemberForm(request.POST)
        if form.is_valid():
            Station.objects.get(pk=pk).members.add(
                form.cleaned_data['user']
            )
            
        return HttpResponseRedirect(reverse("home_station",
                                            kwargs={'pk':pk},
                                        )
                                )

class MemberRemove(View):
    def get(self, request):
        raise Http404

    def post(self, request, pk):
        form = RemoveMemberForm(request.POST)
        if form.is_valid():
            Station.objects.get(pk=pk).members.remove(
                form.cleaned_data['member']
            )
            return HttpResponseRedirect(reverse("home_station",
                                                kwargs={'pk':pk},
                                            )
                                    )

class StationEdit(View):
    def get(self, request):
        raise Http404

    def post(self, request, pk):
        form = StationForm(request.POST)
        if form.is_valid():
            station = Station.objects.get(pk=pk)
            station.name = form.cleaned_data['name']
            station.address = form.cleaned_data['address']
            station.save()
            return HttpResponseRedirect(reverse("home_station",
                                                kwargs={'pk':pk},
                                            )
                                    )

class StationDelete(View):
    def get(self, request):
        raise Http404

    def post(self, request, pk):
        station = Station.objects.get(pk=pk).delete()
        return HttpResponseRedirect(
            reverse("list_create_station")                      
            )
                                                
class ChannelListCreate(View):
    pass

#class ChannelCreate(CreateView):
#    model = Channel
#    fields = ["c_name","c_frequency"]
#
#    def form_valid(self, form):
#        # Check if the station object already exists
#        prev = Channel.objects.filter(c_name=form.instance.c_name)
#        if prev:
#            return redirect("viewchannel", pk=prev[0].pk)
#        return super(ChannelCreate, self).form_valid(form)

#class ChannelHome(DetailView):
#   model = Channel

#class ChannelEdit(UpdateView):
#    model = Channel
#    fields = ["c_name","c_frequency"]
#    template_name_suffix = '_edit_form'
#
#    def get_object(self, queryset=None):
#        obj = Channel.objects.get(pk=self.kwargs['pk'])
#        return obj

#class ListChannels(ListView):
#    model = Channel

##To Alen, All channel related views here

class AudioFileListUpload(View):
    def get(self, request):
        audio_files = AudioFile.objects.filter(uploader=request.user)
        return render(request, 
                      'list_audio_files.html', 
                      {'audio_files':audio_files})

    def post(self, request):
        form = AudioFileForm()
        return render(request, 
                      'upload_audio_file.html', 
                      {'form':form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AudioFileListUpload, self).dispatch(*args, **kwargs)

class AudioActualUpload(View):
    def get(self, request):
        raise Http404
        
    def post(self, request):
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save(commit=False)
            audio_file.uploader = request.user
            audio_file.save()
            return HttpResponseRedirect(
                reverse('home_audio',kwargs={'pk':audio_file.pk})
                )
        else:
            return HttpResponse(form.errors)

class AudioFileHome(View):
    def get(self, request, pk):
        return HttpResponse("Ippa sheriyakkithara:)")
    def post(self, request, pk):
        pass
