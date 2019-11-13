from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.db.models import Count

from akpsi_core.models import (
    Member, Officer, Semester, Chapter, College
)
from akpsi_core.models_ext import (
    MemberBetaChiActives, MemberBetaChiAlumni, MemberBetaChiPledges
)

import pandas as pd

# helper functions
def get_uniques(all_values):
    assert type(all_values) == list

    unique_list = []
    for v in all_values:
        if v not in unique_list:
            unique_list.append(v)
    
    return unique_list

def get_count_of_unique(all_values, unique_values):
    assert type(all_values) == list, "All values must be a list"
    assert type(unique_values) == list, "Unique values must be a list"

    counts = {}
    for uv in unique_values:
        count = 0
        for av in all_values:
            if av == uv:
                count += 1
        counts.update({uv: count})
    
    return counts

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
    if not request.user.is_staff:
        return HttpResponseForbidden()

    template = 'akpsi_core/officers/officer_home.html'
    context = {}

    return render(request, template, context)

def currentRoster(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    template = "akpsi_core/officers/current_roster.html"
    roster = MemberBetaChiActives
    context = {
        'roster': roster
    }

    return render(request, template, context)

def alumniRoster(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    template = "akpsi_core/officers/alumni_roster.html"
    roster = MemberBetaChiAlumni
    context = {
        'roster': roster
    }

    return render(request, template, context)

def pledgeRoster(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    template = "akpsi_core/officers/pledge_roster.html"
    roster = MemberBetaChiPledges
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

def majors(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    template = 'akpsi_core/officers/majors.html'
    context = {
        'major_counts': [],
        'college_counts': []
    }

    # Get a count of each major
    majors = MemberBetaChiActives.order_by('major').values_list('major')

    unique_majors = []
    for m in majors:
        if m not in unique_majors:
            unique_majors.append(m)
    
    for um in unique_majors:
        count = 0
        for ma in majors:
            if ma == um:
                count += 1
        context['major_counts'].append((um[0], count))
    
    # get a count of each senior college
    colleges = MemberBetaChiActives.values('major__college')
    
    unique_colleges = []
    for col in colleges:
        college = col['major__college']
        if college not in unique_colleges:
            unique_colleges.append(college)

    for col in unique_colleges:
        count = 0
        for co in colleges:
            if co['major__college'] == col:
                count += 1
        context['college_counts'].append((col, count))

    return render(request, template, context)

def major_detais(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    template = "akpsi_core/officers/major_detail.html"
    roster = MemberBetaChiActives.filter(major=pk)
    context = {
        "roster": roster,
        "major": pk
    }
    return render(request, template, context)


def pledge_classes(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    template = "akpsi_core/officers/pledge_classes.html"
    context = {
        'class_count': {}
    }

    pledge_classes = MemberBetaChiActives.values('pledge_semester')
    pledge_classes = [i['pledge_semester'] for i in pledge_classes]

    unique_classes = []
    for i in pledge_classes:
        if i not in unique_classes:
            unique_classes.append(i)
        
    for clas in unique_classes:
        count = 0
        for i in pledge_classes:
            if i == clas:
                count += 1
        context['class_count'].update({clas: count})

    return render(request, template, context)

def grad_classes(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    template = "akpsi_core/officers/grad_classes.html"
    context = {
        'class_count': {}
    }

    grad_classes = MemberBetaChiActives.values('graduate_semester')
    grad_classes = [i['graduate_semester'] for i in grad_classes]

    unique_classes = get_uniques(grad_classes)
        
    for clas in unique_classes:
        count = 0
        for i in grad_classes:
            if i == clas:
                count += 1
        context['class_count'].update({clas: count})

    return render(request, template, context)

def alumnus_details(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    template = "akpsi_core/officers/alumnus_details.html"

    # get alumnus object and ensure it is an alum
    alum = get_object_or_404(Member, member_code=pk)
    if alum.akpsi_status != 'Alumnus':
        return HttpResponseNotFound()

    context = {
        'bro': alum
    }

    return render(request, template, context)

def careers(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    template = "akpsi_core/officers/work_tables.html"
    context = {}

    relevant_members = Member.objects.filter(work_company__isnull = False, akpsi_status__in=['Collegiate', 'Alumnus', 'Pledge'])

    # get list of companies ordered by number of people
    companies = relevant_members.values('work_company')
    companies = [i['work_company'] for i in companies]

    unique_companies = get_uniques(companies)
    company_counts = get_count_of_unique(companies, unique_companies)
    
    companies = pd.Series(company_counts)
    context.update({'companies': companies.sort_values(ascending=False).items()})

    # get list of cities ordered by number of people
    cities = relevant_members.values('work_city')
    cities = [i['work_city'] for i in cities]

    unique_cities = get_uniques(cities)
    city_counts = get_count_of_unique(cities, unique_cities)

    cities = pd.Series(city_counts)
    context.update({'cities': cities.sort_values(ascending=False).items()})

    # get list of states ordered by number of people
    states = relevant_members.values('work_state')
    states = [i['work_state'] for i in states]

    unique_states = get_uniques(states)
    state_counts = get_count_of_unique(states, unique_states)

    states = pd.Series(state_counts)
    context.update({"states": states.sort_values(ascending=False).items()})

    return render(request, template, context)
