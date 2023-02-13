from django import forms
from django.core.exceptions import ValidationError

from ibd_website.models import User


class RegisterForm(forms.Form):

    username = forms.CharField(label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Imię")
    last_name = forms.CharField(label="Nazwisko")
    email = forms.EmailField(label="Adres email")
    role = forms.ChoiceField(label="Kim jestem?",
                             choices=(('patient', 'pacjentem'), ('doctor', 'lekarzem')),
                             widget=forms.RadioSelect)

    def clean(self):  # rozbudowujemy metode rodzica
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Podane hasla nie sa takie same!")
            # wyswietla sie na samej gorze, jak zrobic zeby bylo nad password?

    def clean_login(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError("Podana nazwa użytkownika jest juz w bazie!")
        return username


class PatientForm(forms.Form):

    date_of_birth = forms.DateField(label="data urodzenia")
    medical_history = forms.CharField(label="moja historia", widget=forms.Textarea)
    children = forms.ChoiceField(label="czy masz dzieci?",
                                 choices=((True, 'tak'), (False, 'nie')))
    stoma = forms.ChoiceField(label="czy masz stomie?",
                              choices=((True, 'tak'), (False, 'nie')))
    visible = forms.ChoiceField(label="czy chcesz być widoczna dla innych użytkowników?",
                                choices=((True, 'tak'), (False, 'nie')))


class DoctorForm(forms.Form):

    specialization = forms.CharField(label="specjalizacja", required=True)
    experience = forms.CharField(label="doświadczenie", widget=forms.Textarea)


class LoginForm(forms.Form):

    username = forms.CharField(label="nazwa użytkownika")
    password = forms.CharField(label="hasło", widget=forms.PasswordInput)
