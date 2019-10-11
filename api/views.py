from django.http import HttpResponseForbidden
from django.shortcuts import render

from akpsi_core.models import *
from akpsi_core.models_ext import *

import datetime

# Create your views here.

def semester_table(request):
    template = 'api/semester_table.html'

    now = datetime.datetime.now()
    year = now.year.__str__()

    semesters = Semester.objects.filter(
        semester_year__gte='2009',
        semester_year__lte=year
    )
    context = {
        'semesters': semesters
    }

    return render(request, template, context)
