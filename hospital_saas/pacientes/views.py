from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Paciente
from .forms import PacienteForm
import json

class LoginRequiredHTMXMixin(LoginRequiredMixin):
    """
    Mixin para manejar redirecciones en peticiones HTMX cuando el usuario no está autenticado
    """
    def handle_no_permission(self):
        if self.request.htmx:
            return HttpResponse(
                status=204,
                headers={
                    'HX-Redirect': reverse('login_medico')
                }
            )
        return super().handle_no_permission()

def check_htmx_auth(view_func):
    """
    Decorator para manejar autenticación en vistas HTMX
    """
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.htmx:
                return HttpResponse(
                    status=204,
                    headers={
                        'HX-Redirect': reverse('login_medico')
                    }
                )
            return redirect('login_medico')
        return view_func(request, *args, **kwargs)
    return wrapped_view

@check_htmx_auth
def lista_pacientes(request):
    """
    Display a list of all registered patients.
    Redirige al login si el usuario no está autenticado.
    """
    pacientes = Paciente.objects.filter(creado_por=request.user)  # Solo pacientes del médico actual
    if request.htmx:
        return render(request, 'pacientes/partials/lista_pacientes.html', {'pacientes': pacientes})
    return render(request, 'pacientes/lista_pacientes.html', {'pacientes': pacientes})

@check_htmx_auth
def crear_paciente(request):
    """
    Handle patient creation through HTMX form submission.
    Redirige al login si el usuario no está autenticado.
    """
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.creado_por = request.user
            paciente.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        'pacienteActualizado': True,
                        'showMessage': 'Paciente creado exitosamente'
                    })
                }
            )
        return render(request, 'pacientes/partials/formulario_paciente.html', 
                    {'form': form}, status=400)

    form = PacienteForm()
    return render(request, 'pacientes/partials/formulario_paciente.html', 
                {'form': form})

@check_htmx_auth
def editar_paciente(request, pk):
    """
    Handle patient editing through HTMX form submission.
    Redirige al login si el usuario no está autenticado.
    """
    paciente = get_object_or_404(Paciente, pk=pk, creado_por=request.user)  # Solo permite editar pacientes propios
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        'pacienteActualizado': True,
                        'showMessage': 'Paciente actualizado exitosamente'
                    })
                }
            )
        return render(request, 'pacientes/partials/formulario_paciente.html', 
                    {'form': form}, status=400)

    form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/partials/formulario_paciente.html', 
                {'form': form})

@check_htmx_auth
def eliminar_paciente(request, pk):
    """
    Handle patient deletion through HTMX request.
    Redirige al login si el usuario no está autenticado.
    """
    paciente = get_object_or_404(Paciente, pk=pk, creado_por=request.user)  # Solo permite eliminar pacientes propios
    paciente.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                'pacienteActualizado': True,
                'showMessage': 'Paciente eliminado exitosamente'
            })
        }
    )