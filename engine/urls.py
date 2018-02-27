from django.conf.urls import url

from engine import views

urlpatterns = [
    url(r'^$', views.CityListView.as_view(), name='main'),
    url(r'^remove_city/$', views.remove_city, name='remove_city'),
    url(r'^city/$', views.get_temp_for_current_city, name='get_temp_for_current_city')
]
