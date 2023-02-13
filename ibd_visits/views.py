from django.contrib import messages
from django.shortcuts import render
from django.views import View

from ibd_visits.forms import *
from ibd_visits.models import *
from ibd_website.models import *


# # # PROSTY ROBOCZY WIDOK DO DODAWANIA LEKARZOM WOLNYCH TERMINÓW # # #
class AddVisitView(View):
    def get(self, request):
        form = AddVisitForm()
        return render(request, 'add_visit.html', {'form': form})

    def post(self, request):
        form = AddVisitForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            id_doc = data.get('doctor')
            visit_date = data.get('date')
            visit_time = data.get('time')

            visit_term = VisitTerm.objects.create(date=visit_date, time=visit_time)
            doctor = Doctor.objects.get(doctor_id=User.objects.get(id=id_doc))

            DoctorVisit.objects.create(doctor=doctor, visit_term=visit_term)

            messages.success(request, f"Pomyślnie dodano wizytę dnia {visit_date} "
                                      f"o godz {TIME[int(visit_time) - 1][1]} "
                                      f"lekarzowi: {doctor.doctor.first_name} {doctor.doctor.last_name}!")

            return render(request, 'add_visit.html', {'form': form})

        else:

            messages.error(request, "Błąd - nie dodano żadnej wizyty!")

            return render(request, 'add_visit.html', {'form': form})
