from django import forms
from .models import *

class ClassBaseForm(forms.Form):
    classbase = forms.ModelChoiceField(queryset=Class_Base.objects.all())

class RaceForm(forms.Form):
    race = forms.ModelChoiceField(queryset=Race.objects.all())