from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.decorators.http import require_POST
import geocoder
from .models import City
from weather import Weather, Unit


# при добавлении нового города обновлять список get_cities_list
# при нажатии на Город (your location) открывать погоду города
# сделать красиво на главной странице
# рефакторинг
# classbaseview
# комментарии


weather = Weather(unit=Unit.CELSIUS)


def get_current_weather(city):
    try:
        location = weather.lookup_by_location(city)
        condition = location.condition()
        return condition
    except:
        return None


def get_future_weather(city):
    try:
        location = weather.lookup_by_location(city)
        forecasts = location.forecast()
        return forecasts[0:5]
    except:
        return None


class CityListView(generic.ListView):
    model = City
    context_object_name = 'cities'
    template_name = "engine/base.html"

    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data()
        return context

    def get_queryset(self):
        return City.objects.order_by('-pk')


@require_POST
def location_weather(request):
    latitude = request.POST.get('latitude', '')
    longitude = request.POST.get('longitude', '')
    city = None
    while city is None:
        g = geocoder.google([latitude, longitude], method='reverse')
        city = g.city
    current = get_current_weather(city)
    future = get_future_weather(city)
    return render(request, "engine/location_weather.html", {"city": city, 'current': current, 'forecasts': future})



@require_POST
def add_city(request):
    city = request.POST.get('city', '')
    if get_current_weather(city):
        try:
            get_current_weather(city)
            city = City.objects.create(name=city)
            return HttpResponse(city.pk)
        except:
            None
    return HttpResponse("None")


@require_POST
def get_city(request):
    city = request.POST.get('city', '')
    current = get_current_weather(city)
    future = get_future_weather(city)
    return render(request, "engine/city_weather.html", {'city': city, 'current': current, 'forecasts': future})


def remove_city(request):
    pk = int(request.GET.get("pk", 0))
    song = get_object_or_404(City, pk=pk)
    song.delete()
    return redirect("/")
