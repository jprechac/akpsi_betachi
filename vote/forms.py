from django import forms
from .models import Vote


class VotingForm(forms.Form):
    chosen_members_options = forms.MultipleChoiceField(choices=[], label='AKPsi', required=False,
                                                     widget=forms.SelectMultiple(
                                                        attrs={
                                                             'class': 'form-control'
                                                         }
                                                     ))
    other_member_name = forms.CharField(label='Other', max_length=100, required=False,
                                      widget=forms.TextInput(
                                        attrs={
                                              'class': 'form-control',
                                              'placeholder': 'Anybody else you would like to nominate?'
                                          }
                                      ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_members_names = Vote.objects.order_by('member_name').values_list('member_name', flat=True).distinct()
        self.fields['chosen_members_options'].choices = [(member_name, member_name) for member_name in unique_member_names]# from .models import
