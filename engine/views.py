from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import City
# from weather import Weather, Unit


API_KEY = "94884ca874fb222e46084a95c6703bb8307dba79"


class CityListView(generic.ListView):
    model = City
    context_object_name = 'cities'
    template_name = "engine/base.html"

    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data()
        last_city = City.objects.last()
        context['last_city'] = last_city if last_city else None
        get_weather_for_city("moscow,RU")
        return context

    def get_queryset(self):
        return City.objects.order_by('-pk')


def get_weather_for_city(city):
    weather = Weather(unit=Unit.CELSIUS)
    lookup = weather.lookup(560743)
    condition = lookup.condition()
    print(condition.text())
