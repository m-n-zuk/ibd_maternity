import pytest
from django.test import Client
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
    user = User.objects.create_user(username='test_user',
                                    password='test_pass')
    return user


@pytest.fixture
def admin():
    admin = User.objects.create_superuser(username='admin_username',
                                          email='admin@admin.pl',
                                          password='admin_pass')
    return admin


@pytest.fixture
def doctor():
    doctor = User.objects.create_user(username='test_user_1',
                                      password='test_pass_1')
    Doctor.objects.create(doctor=doctor,
                          specialization='test_specialization',
                          experience='test_experience')
    return doctor


@pytest.fixture
def patient():
    patient = User.objects.create_user(username='test_user_2',
                                       password='test_pass_2')
    Patient.objects.create(patient=patient,
                           date_of_birth='1990-01-20',
                           medical_history='test_medical_history_2',
                           children=True, stoma=True, visible=True)
    return patient


# --------------------------- #
# -------- T E S T S -------- #
# --------------------------- #
@pytest.mark.django_db
def test_add_visit_1(client, user):
    response = client.get('/add_visit/')
    assert response.status_code == 302

    client.login(username='test_user', password='test_pass')
    response = client.get('/add_visit/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_visit_2(client, admin):
    client.force_login(admin)
    response = client.get('/add_visit/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_visit_1(client, doctor, patient):

    response = client.get(f'/book_visit/{doctor.id}/{patient.id}')
    assert response.status_code == 302


@pytest.mark.django_db
def test_book_visit_2(client, doctor, patient):

    client.force_login(patient)
    response = client.get(f'/book_visit/{doctor.id}/{patient.id}')
    assert response.status_code == 200


@pytest.mark.django_db
def test_visits_1(client, user):

    response = client.get(f'/visits/{user.id}')
    assert response.status_code == 302
    assert response.url == '/login/?next=' + f'/visits/{user.id}'


@pytest.mark.django_db
def test_visits_2(client, user):

    client.force_login(user)
    response = client.get(f'/visits/{user.id}')
    assert response.status_code == 200
