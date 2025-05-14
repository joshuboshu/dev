# medicos/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Medico(AbstractUser):
    ESPECIALIDADES = [
        ('PEDIATRIA', 'Pediatría'),
        ('CARDIOLOGIA', 'Cardiología'),
        ('DERMATOLOGIA', 'Dermatología'),
    ]
    
    especialidad = models.CharField(
        max_length=50,
        choices=ESPECIALIDADES,
        default='PEDIATRIA'
    )
    telefono = models.CharField(max_length=20, blank=True)
    matricula = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.get_full_name()} - {self.especialidad}"

    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'