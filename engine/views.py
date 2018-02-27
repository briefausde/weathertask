from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.decorators.http import require_POST

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
            context['last_weather'] = get_current_weather(last_city)
            context['forecasts'] = get_future_weather(last_city)
        return context

    def get_queryset(self):
        return City.objects.order_by('-pk')


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


@require_POST
def get_temp_for_current_city(request):
    city = request.POST.get('city', '')
    current = get_current_weather(city)
    future = get_future_weather(city)
    if current:
        try:
            City.objects.create(name=city)
        except:
            None
        return render(request, "engine/city_weather.html", {'city': city, 'temp': current.temp(), 'text': current.text(), 'forecasts': future})
    return render(request, "engine/city_weather.html", {"error": "We can't find this city"})


def remove_city(request):
    pk = int(request.GET.get("pk", 0))
    song = get_object_or_404(City, pk=pk)
    song.delete()
    return redirect("/")


def city_list(request):
    cities = City.objects.order_by('-pk')
    return render(request, "engine/city_list.html", {'cities': cities})
