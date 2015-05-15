from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
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
from .forms import UserCreateForm, StationForm

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
        return HttpResponse("Created :)")

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
