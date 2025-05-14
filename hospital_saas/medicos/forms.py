from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Medico

class MedicoCreationForm(UserCreationForm):
    class Meta:
        model = Medico
        fields = ('username', 'first_name', 'last_name', 'email', 
                 'especialidad', 'telefono', 'matricula', 'password1', 'password2')

class MedicoLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)