from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    cedula = models.CharField(max_length=20, unique=True)
    alergias = models.TextField(blank=True, default="Ninguna")
    antecedentes = models.TextField(blank=True, default="Ninguno")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    fecha = models.DateTimeField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)