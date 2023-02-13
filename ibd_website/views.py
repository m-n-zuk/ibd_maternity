from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from ibd_website.forms import *
from ibd_website.models import *


class MainView(View):
    def get(self, request):
        return render(request, 'main_page.html')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):

        form = RegisterForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # niebezpieczna operacja (C z CRUD)
            user = User.objects.create_user(
                username=data.get('username'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                password=data.get('password')
            )
            role = data.get('role')

            return redirect(f"/register_details/{role}/{user.id}")

        else:  # dodac po dodaniu walidacji
            return render(request, 'register.html', {'form': form})


class RegisterDetailsView(View):
    def get(self, request, role, id):

        if role == 'patient':
            form = PatientForm()
        if role == 'doctor':
            form = DoctorForm()
        return render(request, 'register_details.html', {'form': form, 'role': role})

    def post(self, request, role, id):

        if role == 'patient':
            form = PatientForm(request.POST)

            if form.is_valid():

                data = form.cleaned_data

                user = User.objects.get(id=id)

                patient_details = Patient.objects.create(
                    patient=user,
                    date_of_birth=data.get('date_of_birth'),
                    medical_history=data.get('medical_history'),
                    children=data.get('children'),
                    stoma=data.get('stoma'),
                    visible=data.get('visible')
                )

                return redirect(f"/login/")

            else:  # dodac po dodaniu walidacji
                return render(request, 'register_details.html', {'form': form, 'role': role})

        if role == 'doctor':
            form = DoctorForm(request.POST)

            if form.is_valid():

                data = form.cleaned_data

                user = User.objects.get(id=id)

                doctor_details = Doctor.objects.create(
                    doctor=user,
                    experience=data.get('experience'),
                    specialization=data.get('specialization')
                )

                return redirect(f"/login/")

            else:  # dodac po dodaniu walidacji
                return render(request, 'register_details.html', {'form': form, 'role': role})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')
            password = data.get('password')

            # uwierzytelnienie
            user = authenticate(username=username, password=password)

            if user:
                # logowanie
                login(request, user)

                return redirect(f"/user")

            else:
                messages.error(request, 'Błąd uwierzytelnienia. Podano nieprawidłowe poświadczenia.')

                return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(f"/")
