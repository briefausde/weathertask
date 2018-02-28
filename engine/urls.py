from django.conf.urls import url

from engine import views

urlpatterns = [
    url(r'^$', views.CityListView.as_view(), name='main'),
    url(r'^remove_city/$', views.remove_city, name='remove_city'),
    url(r'^add_city/$', views.add_city, name='add_city'),
    url(r'^get_city/$', views.get_city, name='get_city'),
    url(r'^location_weather/$', views.location_weather, name='location_weather')
]
