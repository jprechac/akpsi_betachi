from django.urls import path, re_path
from . import views
from .views import HomeView

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^officer/$', views.officerHomeView, name="officer_home"),
    re_path(r'^officer/current_roster$', views.currentRoster, name='current_roster'),
    re_path(r'^(?P<pk>[A-Za-z0-9]{8})$', views.bro_details, name="bro_details"),
]
