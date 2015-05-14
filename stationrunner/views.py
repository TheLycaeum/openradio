from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
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

@login_required
def user_redirect(request):
    url = reverse('userhome', kwargs={'pk':request.user.id})
    return HttpResponseRedirect(url)

class UserHome(DetailView):
    model = User
    template_name_suffix = "_home"

    def get_object(self, queryset=None):
        return self.request.user

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserHome, self).dispatch(*args, **kwargs)

class StationListCreate(View):
    def get(self, request):
        return HttpResponse('get')

    def post(self, request):
        return HttpResponse('post')

class StationHome(DetailView):
    model = Station

class StationEdit(UpdateView):
    model = Station
    fields = ["name","address"]
    template_name_suffix = '_edit_form'

    def get_object(self, queryset=None):
        obj = Station.objects.get(pk=self.kwargs['pk'])
        return obj

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
