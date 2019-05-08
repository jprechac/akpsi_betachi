from django import forms
from .models import Member, Semester

class MemberForm(forms.ModelForm):
    class Meta:
        pass

class SemesterForm(forms.ModelForm):
    class Meta:
        pass
