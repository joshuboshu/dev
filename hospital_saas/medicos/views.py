from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MedicoCreationForm, MedicoLoginForm

def registrar_medico(request):
    if request.method == 'POST':
        form = MedicoCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_medico')
    else:
        form = MedicoCreationForm()
    return render(request, 'medicos/registro.html', {'form': form})

def login_medico(request):
    if request.method == 'POST':
        form = MedicoLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_pacientes')
    else:
        form = MedicoLoginForm()
    return render(request, 'medicos/login.html', {'form': form})

@login_required
def logout_medico(request):
    logout(request)
    return redirect('login_medico')