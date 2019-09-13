from django.shortcuts import render

from .forms import VotingForm
from .models import Vote
def index(request):
    if request.method == 'POST':
        form = VotingForm(request.POST)
    if form.is_valid():
        chosen_members_options = form.cleaned_data.get('chosen_members_options', [])
        other_member_name = form.cleaned_data.get('other_member_name', '')
        Vote.bulk_vote(chosen_members_options + [other_member_name])
        message = 'Thank You For Voting!'
    elif request.method == 'GET':
        message = ''
    form = VotingForm()
    return render(request, 'templates/survey.html', {'form': form, 'message': message})# Create your views here.
