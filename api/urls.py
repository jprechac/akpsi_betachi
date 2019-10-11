from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^asu49fjqi.816sf3f$', views.semester_table, name="semester_api"),
]
