from django import forms

from ibd_visits.models import *
from ibd_website.models import *


class AddVisitForm(forms.Form):

    doctors = User.objects.filter(doctor__isnull=False)

    CHOICE = (
        (doctor.id, f"{doctor.first_name} {doctor.last_name}") for doctor in doctors
    )

    doctor = forms.ChoiceField(choices=CHOICE)
    date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.ChoiceField(choices=TIME)

