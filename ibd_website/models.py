from django.contrib.auth.models import AbstractUser
from django.db import models

from ibd_visits.models import DoctorVisit, VisitTerm


class User(AbstractUser):
    phone_number = models.IntegerField(null=True)


class Patient(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=False)
    medical_history = models.TextField(null=True)
    children = models.BooleanField(null=True)
    stoma = models.BooleanField(null=False)
    visible = models.BooleanField(null=False)


class Illness(models.Model):
    patient_details = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    diagnosis_date = models.DateField(null=True)


class Doctor(models.Model):
    doctor = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.TextField(null=False)
    specialization = models.CharField(max_length=200, null=False)
    visit_term = models.ManyToManyField(VisitTerm, through=DoctorVisit)
