from django import forms

from ibd_visits.models import *
from ibd_website.models import *


class AddVisitForm(forms.Form):

    doctor = forms.ChoiceField(choices=tuple())
    date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.ChoiceField(choices=TIME)
#
#
# class BookVisitForm(forms.Form):
#
#     term = forms.ChoiceField(choices=[])
