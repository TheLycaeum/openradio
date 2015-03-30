from django.views.generic.edit import CreateView
from .models import Station

class StationCreate(CreateView):
    model = Station
    fields = ["name"]
