from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from akpsi_core.models import (
    Member, Officer, Semester, Chapter
)

# Create your views here.
class HomeView(TemplateView):
    """
    Landing page for the app.
    """
    template_name = 'akpsi_core/home.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        This function will expand the information that can be sent to the
        template to use in the in-line python.
        You can send objects, lists, dataframes, integers, pretty much whatever.
        """
        context = super().get_context_data(**kwargs)
        return context

def officerHomeView(request):
    template = 'akpsi_core/officers/officer_home.html'
    context = {}
    if request.user.is_staff:
        return render(request, template, context)
    else:
        return HttpResponseForbidden()

def currentRoster(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    template = "akpsi_core/officers/current_roster.html"
    roster = Member.objects.filter(akpsi_status='Collegiate', chapter='Beta Chi')
    context = {
        'roster': roster
    }

    return render(request, template, context)

def bro_details(request, pk):
    template = "akpsi_core/officers/bro_details.html"
    bro = get_object_or_404(Member, member_code=pk)

    context = {
        'bro': bro
    }

    return render(request, template, context)
