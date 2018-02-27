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
            context['last_weather'] = get_weather_for_city(last_city)
        return context

    def get_queryset(self):
        return City.objects.order_by('-pk')


def get_weather_for_city(city):
    try:
        location = weather.lookup_by_location(city)
        condition = location.condition()
        return condition.temp()
    except:
        return None


@require_POST
def get_temp_for_current_city(request):
    city = request.POST.get('city', '')
    temp = get_weather_for_city(city)
    if temp:
        City.objects.create(name=city)
        return render(request, "engine/city.html", {'temp': temp})
    return render(request, "engine/city.html", {"error": "We can't find this song"})


def remove_city(request):
    pk = int(request.GET.get("pk", 0))
    song = get_object_or_404(City, pk=pk)
    song.delete()
    return redirect("/")
