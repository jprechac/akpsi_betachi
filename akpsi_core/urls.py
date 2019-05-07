from django.urls import path
from . import views
from .views import HomeView

urlpatterns = [
    path('core/', HomeView.as_view(), name='home'),
]
