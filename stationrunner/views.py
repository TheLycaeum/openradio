from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Station, Channel
from .forms import UserCreateForm

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

class UserLogin(FormView):
    form_class = AuthenticationForm
    template_name = "auth/login.html"

class UserHome(DetailView):
    model = User
    template_name_suffix = "_home"
    
class StationCreate(CreateView):
    model = Station
    fields = ["name","address"]

    def form_valid(self, form):
        # Check if the station object already exists
        prev = Station.objects.filter(name=form.instance.name)
        if prev:
            return redirect("viewstation", pk=prev[0].pk)
        return super(StationCreate, self).form_valid(form)

class StationHome(DetailView):
    model = Station

class StationEdit(UpdateView):
    model = Station
    fields = ["name","address"]
    template_name_suffix = '_edit_form'

    def get_object(self, queryset=None):
        obj = Station.objects.get(pk=self.kwargs['pk'])
        return obj
    
class ListStations(ListView):
    model = Station


class ChannelCreate(CreateView):
    model = Channel
    fields = ["c_name","c_frequency"]

    def form_valid(self, form):
        # Check if the station object already exists
        prev = Channel.objects.filter(c_name=form.instance.c_name)
        if prev:
            return redirect("viewchannel", pk=prev[0].pk)
        return super(ChannelCreate, self).form_valid(form)

class ChannelHome(DetailView):
    model = Channel

class ChannelEdit(UpdateView):
    model = Channel
    fields = ["c_name","c_frequency"]
    template_name_suffix = '_edit_form'

    def get_object(self, queryset=None):
        obj = Channel.objects.get(pk=self.kwargs['pk'])
        return obj

class ListChannels(ListView):
    model = Channel
