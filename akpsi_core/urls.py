from django.urls import path, re_path
from . import views
from .views import HomeView

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^officer/$', views.officerHomeView, name="officer_home"),
    re_path(r'^officer/current_roster$', views.currentRoster, name='current_roster'),
    re_path(r'^officer/alumni_roster$', views.alumniRoster, name='alumni_roster'),
    re_path(r'^officer/majors$', views.majors, name="majors"),
    re_path(r'^officer/pledge-classes$', views.pledge_classes, name="pledge_classes"),
    re_path(r'^officer/grad-classes$', views.grad_classes, name="grad_classes"),
    re_path(r'^active/(?P<pk>[A-Za-z0-9().]{8})$', views.bro_details, name="bro_details"),
    re_path(r'^alumnus/(?P<pk>[A-Za-z0-9().]{4,8})$', views.alumnus_details, name="alum_detail"),
]
