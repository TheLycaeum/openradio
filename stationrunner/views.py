from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from .models import Station

class StationCreate(CreateView):
    model = Station
    fields = ["name","address"]

    def form_valid(self, form):
        # Check if the station object already exists
        prev = Station.objects.filter(name=form.instance.name)
        if prev:
            return redirect("viewstation", pk=prev[0].pk)
        return super(StationCreate, self).form_valid(form)

class StationView(DetailView):
    model = Station

class StationEdit(UpdateView):
    model = Station
    fields = ["name","address"]
    template_name_suffix = '_edit_form'

    def get_object(self, queryset=None):
        obj = Station.objects.get(id=self.kwargs['id'])
        return obj
    
