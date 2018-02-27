from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import City
from weather import Weather, Unit


weather = Weather(unit=Unit.CELSIUS)


class CityListView(generic.ListView):
    model = City
    context_object_name = 'cities'
    template_name = "engine/base.html"

    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data()
        last_city = City.objects.last()
        if last_city:
            context['last_city'] = last_city
            context['last_weather'] = get_weather_for_city(last_city)
        return context

    def get_queryset(self):
        return City.objects.order_by('-pk')


def get_weather_for_city(city):
    location = weather.lookup_by_location(city)
    condition = location.condition()
    return condition.temp()
