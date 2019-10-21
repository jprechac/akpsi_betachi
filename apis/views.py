from django.shortcuts import render
from rest_framework import viewsets
from datetime import datetime

from .serializers import *
from akpsi_core import models as core_models

# Create your views here.
year = datetime.now().year

class SemesterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and changing semester data
    """
    queryset = core_models.Semester.objects.filter(
        semester_year__gte=2008,
        semester_year__lte=year
    )
    serializer_class = SemesterSerializer