import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from ibd_visits.forms import *
from ibd_visits.models import *
from ibd_website.models import *


# view for adding visits to doctors - only for admin
class AddVisitView(PermissionRequiredMixin, View):
    permission_required = 'add_doctorvisit'

    def get(self, request):

        doctors = User.objects.filter(doctor__isnull=False)
        return render(request, 'add_visit.html', {'doctors': doctors, 'time': TIME})

    def post(self, request):

        doctor_id = request.POST['doctor']
        visit_date = request.POST['date']
        visit_time = request.POST['time']

        visit_term = VisitTerm.objects.create(date=visit_date, time=visit_time)
        doctor = Doctor.objects.get(doctor_id=User.objects.get(id=doctor_id))

        DoctorVisit.objects.create(doctor=doctor, visit_term=visit_term)

        messages.success(request, f"Pomyślnie dodano wizytę dnia {visit_date} "
                                  f"o godz {TIME[int(visit_time) - 1][1]} "
                                  f"lekarzowi: {doctor.doctor.first_name} {doctor.doctor.last_name}!")

        return redirect('/add_visit/')


# class AddVisitView2(PermissionRequiredMixin, View):
#     permission_required = 'add_doctorvisit'
#
#     doctors = User.objects.filter(doctor__isnull=False)
#
#     doc = (
#         (doctor.id, f"{doctor.first_name} {doctor.last_name}") for doctor in doctors
#     )
#
#     def get(self, request):
#
#         form = AddVisitForm()
#
#         form.fields['doctor'].choices = self.doc
#
#         return render(request, 'add_visit2.html', {'form': form})
#
#     def post(self, request):
#         form = AddVisitForm(request.POST)
#         form.fields['doctor'].choices = self.doc
#
#         if form.is_valid():
#
#             doctor, date, time, *rest = [*form.cleaned_data.values()]
#
#             visit_term = VisitTerm.objects.create(date=date, time=time)
#             doctor = Doctor.objects.get(doctor_id=User.objects.get(id=doctor))
#
#             DoctorVisit.objects.create(doctor=doctor, visit_term=visit_term)
#
#             messages.success(request, f"Pomyślnie dodano wizytę dnia {date} "
#                                       f"o godz {TIME[int(time) - 1][1]} "
#                                       f"lekarzowi: {doctor.doctor.first_name} {doctor.doctor.last_name}!")
#
#             return render(request, 'add_visit2.html', {'form': form})
#
#         else:
#
#             messages.error(request, "Błąd - nie dodano żadnej wizyty!")
#
#             return render(request, 'add_visit2.html', {'form': form})


# class BookVisitView(LoginRequiredMixin, View):
#
#     def get(self, request, id_doc, id_pat):
#
#         patient = User.objects.get(id=id_pat)
#         doctor = User.objects.get(id=id_doc)
#
#         form = BookVisitForm()
#
#         terms = (
#             (visit.id, f"data: {visit.visit_term.date}, godzina: {TIME[visit.visit_term.time - 1][1]}")
#             for visit in DoctorVisit.objects.filter(doctor=Doctor.objects.get(doctor=doctor), is_free=True)
#         )
#
#         form.fields['term'].choices = terms
#
#         return render(request, 'book_visit.html', {'form': form, 'patient': patient, 'doctor': doctor})
#
#     def post(self, request, id_doc, id_pat):
#
#         form = BookVisitForm(request.POST)
#
#         if form.is_valid():
#
#             data = form.cleaned_data
#
#             visit_id = data.get('term')
#
#             visit_term = DoctorVisit.objects.get(id=visit_id)
#
#             MedicalVisit.objects.create(
#                 patient=User.objects.get(id=id_pat),
#                 doctor=User.objects.get(id=id_doc),
#                 visit_term=visit_term
#             )
#
#             visit_term.is_free = False
#             visit_term.save()
#
#             return redirect(f"/visits/{id_pat}")
#
#         else:
#             return render(request, 'book_visit.html', {'form': form})


# view for booking visits by patients - only for logged-in user
class BookVisitView2(LoginRequiredMixin, View):

    def get(self, request, id_doc, id_pat):
        patient = Patient.objects.get(patient=User.objects.get(id=id_pat))
        doctor = Doctor.objects.get(doctor=User.objects.get(id=id_doc))

        doc_visits = DoctorVisit.objects.filter(doctor=doctor, is_free=True)

        for visit in doc_visits:
            visit.visit_term.time = TIME[visit.visit_term.time - 1][1]

        return render(request, 'book_visit2.html', {'doc_visits': doc_visits, 'patient': patient, 'doctor': doctor})

    def post(self, request, id_doc, id_pat):
        visit_id = request.POST['term']

        visit_term = DoctorVisit.objects.get(id=visit_id)

        MedicalVisit.objects.create(
            patient=User.objects.get(id=id_pat),
            doctor=User.objects.get(id=id_doc),
            visit_term=visit_term
        )

        visit_term.is_free = False
        visit_term.save()

        return redirect(f"/visits/{id_pat}")


# view of all medical visits of logged-in user
class VisitsView(LoginRequiredMixin, View):

    def get(self, request, id):

        patient = User.objects.get(id=id)
        med_visits = MedicalVisit.objects.filter(patient=patient)
        future_visits = []
        past_visits = []

        for med_visit in med_visits:
            med_visit.visit_term.visit_term.time = TIME[med_visit.visit_term.visit_term.time - 1][1]
            if med_visit.visit_term.visit_term.date >= datetime.date.today():
                future_visits.append(med_visit)
            else:
                past_visits.append(med_visit)

        return render(request, 'visits.html', {'med_visits': med_visits, 'past': past_visits, 'future': future_visits})
