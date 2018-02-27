from django.conf.urls import url

from engine import views

urlpatterns = [
    url(r'^$', views.CityListView.as_view(), name='main'),
]
