from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.
class HomeView(TemplateView):
    """
    Landing page for the app.
    """
    template_name = 'akpsi_core/base.html'

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
