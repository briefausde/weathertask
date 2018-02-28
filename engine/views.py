from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import City
from weather import Weather, Unit
import geocoder


# рефакторинг
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


class LocationWeatherView(generic.View):
    template_name = "engine/location_weather.html"

    def get(self, request):
        latitude = request.GET.get('latitude', '')
        longitude = request.GET.get('longitude', '')
        city = None
        while city is None:
            g = geocoder.google([latitude, longitude], method='reverse')
            city = g.city
        current = get_current_weather(city)
        future = get_future_weather(city)
        return render(request, self.template_name, {"city": city, 'current': current, 'forecasts': future})


class AddCityView(generic.View):
    def get(self, request):
        city = request.GET.get('city', '').lower()
        if get_current_weather(city):
            if not City.objects.filter(name=city):
                new_city = City.objects.create(name=city)
                return HttpResponse(new_city.pk)
        return HttpResponse("None")


class GetCityView(generic.View):
    template_name = "engine/city_weather.html"

    def get(self, request):
        city = request.GET.get('city', '')
        current = get_current_weather(city)
        future = get_future_weather(city)
        return render(request, self.template_name, {'city': city, 'current': current, 'forecasts': future})


def remove_city(request):  # функция удаления города из базы
    pk = int(request.GET.get("pk", 0))  # получаем id города
    song = get_object_or_404(City, pk=pk)  # достаем объект "город" с базы
    song.delete()  # удаляем город
    return redirect("/")
