import pytest
from django.contrib.sites import requests
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from ibd_website.models import User, Patient, Doctor


# --------------------------- #
# ----- F I X T U R E S ----- #
# --------------------------- #
@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = User.objects.create_user(username='test_user', password='test_pass')
    return user


@pytest.fixture
def patient(user):
    patient = Patient.objects.create(
        patient=user,
        date_of_birth='1993-10-20',
        medical_history='test_medical_history',
        children=False,
        stoma=True,
        visible=True,
    )
    return patient


@pytest.fixture
def doctor(user):
    doctor = Doctor.objects.create(
        doctor=user,
        specialization='test_specialization',
        experience='test_experience'
    )
    return doctor


# --------------------------- #
# -------- T E S T S -------- #
# --------------------------- #
@pytest.mark.django_db
def test_main_view_1(client):
    response = client.get('/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_main_view_2(client):
    response = client.get('/')

    assert response.status_code == 200
    assert 'main_page.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_register_view_1(client):
    response = client.get('/register/')
    assert response.status_code == 200

    data = {
        'username': 'test_user',
        'email': 'test@email.com',
        'password': 'test_pass',
        'password2': 'test_pass',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'doctor'
    }

    response = client.post('/register/', data=data)
    assert response.status_code == 302
    assert response.url == f'/register_details/doctor/1'


@pytest.mark.django_db
def test_register_view_2(client):
    response = client.get('/register/')
    assert response.status_code == 200

    data = {
        'username': 'test_user',
        'email': 'test@email.com',
        'password': 'test_pass',
        'password2': 'test_pass',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'patient'
    }

    response = client.post('/register/', data=data)
    assert response.status_code == 302
    assert response.url == f'/register_details/patient/2'  # dlaczego nie 1 ?


@pytest.mark.django_db
def test_register_details_view_1(client, user):
    url = f'/register_details/doctor/{user.id}/'
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'specialization': 'test_specialization',
        'experience': 'test_experience'
    }

    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == '/login/'


@pytest.mark.django_db
def test_register_details_view_2(client, user):

    url = f'/register_details/patient/{user.id}/'
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'date_of_birth': '1993-10-20',
        'medical_history': 'test_medical_history',
        'children': False,
        'stoma': True,
        'visible': True
    }

    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == '/login/'


@pytest.mark.django_db
def test_login_view_1(client):
    response = client.get('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_2(client, user):
    response = client.post('/login/', {'username': 'test_user', 'password': 'test_pass'})
    assert response.status_code == 302
    assert response.url == '/user'


@pytest.mark.django_db
def test_logout_view_1(client, user):
    client.login(username='test_user', password='test_pass')
    response = client.get('/logout/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_view_2(client, user):
    client.login(username='test_user', password='test_pass')
    response = client.get('/logout/')
    assert response.url == '/'


@pytest.mark.django_db
def test_user_view_1(client):
    response = client.get('/user/')
    assert response.status_code == 302
    assert response.url == '/login/?next=' + '/user/'


@pytest.mark.django_db
def test_user_view_2(client, user):
    client.login(username='test_user', password='test_pass')
    response = client.get('/user/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_community_view_1(client):
    response = client.get('/community/')
    assert response.status_code == 200
    assert len(response.context['users']) == 0


@pytest.mark.django_db
def test_community_view_2(client, user, patient):
    response = client.get('/community/')
    assert response.status_code == 200

    assert user.patient.visible is True
    assert len(response.context['users']) == 1
    assert response.context['users'][0].id == user.id
    assert response.context['users'][0].patient.date_of_birth == 29

    user2 = User.objects.create_user(username='test_user_2', password='test_pass_2')
    Patient.objects.create(
        patient=user2,
        date_of_birth='1990-01-20',
        medical_history='test_medical_history_2',
        children=True,
        stoma=True,
        visible=True,
    )

    response = client.get('/community/')
    assert response.status_code == 200

    assert user2.patient.visible is True
    assert len(response.context['users']) == 2
    assert response.context['users'][1].id == user2.id
    assert response.context['users'][1].patient.date_of_birth == 33

    user3 = User.objects.create_user(username='test_user_3', password='test_pass_3')
    Patient.objects.create(
        patient=user3,
        date_of_birth='1999-01-20',
        medical_history='test_medical_history_3',
        children=True,
        stoma=True,
        visible=False,
    )

    response = client.get('/community/')
    assert response.status_code == 200

    assert user3.patient.visible is False
    assert len(response.context['users']) == 2


@pytest.mark.django_db
def test_doctors_view_1(client):

    response = client.get('/doctors/')
    assert response.status_code == 200
    assert len(response.context['users']) == 0


@pytest.mark.django_db
def test_doctors_view_2(client, user, doctor):

    response = client.get('/doctors/')
    assert response.status_code == 200

    assert len(response.context['users']) == 1
    assert response.context['users'][0].id == user.id
    assert response.context['users'][0].doctor.specialization == 'test_specialization'
