from django.urls import path, re_path
from . import views
from .views import HomeView

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
]
