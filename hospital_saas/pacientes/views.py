from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Paciente
from .forms import PacienteForm
import json

def lista_pacientes(request):
    """
    Display a list of all registered patients.
    
    Handles both full page requests and HTMX partial requests. When accessed via HTMX,
    returns only the patient list partial template for dynamic updates.

    Args:
        request (HttpRequest): The incoming request object. Checks for HTMX headers.

    Returns:
        HttpResponse: 
            - If HTMX request: Renders 'pacientes/partials/lista_pacientes.html'
            - If normal request: Renders 'pacientes/lista_pacientes.html'
            
    Context:
        pacientes (QuerySet): All patient objects ordered by creation date.
    """
    pacientes = Paciente.objects.all()
    if request.htmx:
        return render(request, 'pacientes/partials/lista_pacientes.html', {'pacientes': pacientes})
    return render(request, 'pacientes/lista_pacientes.html', {'pacientes': pacientes})

def crear_paciente(request):
    """
    Handle patient creation through HTMX form submission.
    
    Processes both initial form display (GET) and form submission (POST). Validates form data
    and returns appropriate responses for both success and error cases.

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse:
            - GET: Displays empty patient form
            - POST (valid): Returns 204 with HTMX triggers
            - POST (invalid): Returns form with errors (status 400)
            
    HTMX Triggers:
        pacienteActualizado: Triggered on successful creation
        showMessage: Contains success notification message
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
        else:
            # Devuelve solo los campos con errores para ahorrar ancho de banda
            return render(request, 'pacientes/partials/formulario_paciente.html', {
                'form': form
            }, status=400)

    form = PacienteForm()
    return render(request, 'pacientes/partials/formulario_paciente.html', {'form': form})

def editar_paciente(request, pk):
    """
    Handle patient editing through HTMX form submission.
    
    Retrieves an existing patient and processes form updates. Handles validation
    and returns appropriate responses for both success and error cases.

    Args:
        request (HttpRequest): The incoming request object.
        pk (int): Primary key of the patient to edit.

    Returns:
        HttpResponse:
            - GET: Displays form pre-populated with patient data
            - POST (valid): Returns 204 with HTMX triggers
            - POST (invalid): Returns form with errors (status 400)
            
    Raises:
        Http404: If no patient exists with the given pk.
        
    HTMX Triggers:
        pacienteActualizado: Triggered on successful update
        showMessage: Contains success notification message
    """
    paciente = get_object_or_404(Paciente, pk=pk)
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
        else:
            return render(request, 'pacientes/partials/formulario_paciente.html', {
                'form': form
            }, status=400)

    form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/partials/formulario_paciente.html', {'form': form})

def eliminar_paciente(request, pk):
    """
    Handle patient deletion through HTMX request.
    
    Deletes the specified patient and triggers list refresh. Designed to work
    with HTMX-powered interfaces.

    Args:
        request (HttpRequest): The incoming request object.
        pk (int): Primary key of the patient to delete.

    Returns:
        HttpResponse: HTTP 204 response with HTMX trigger
        
    Raises:
        Http404: If no patient exists with the given pk.
        
    HTMX Triggers:
        pacienteActualizado: Triggered after successful deletion
    """
    paciente = get_object_or_404(Paciente, pk=pk)
    paciente.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': 'pacienteActualizado'
        }
    )