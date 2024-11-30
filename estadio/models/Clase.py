from django.db import models
from estadio.models import Usuario


class Clase(models.Model):
    clase_profesor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="clase_profesor")
    clase_usuarios = models.ManyToManyField(Usuario, related_name="clase_usuarios")
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=500)
    cupo_total = models.IntegerField()
    cupo_disponible = models.IntegerField()

    ESTADO_OPCIONES = [
        ("activa", "Activa"),
        ("completada", "Completada"),
        ("cancelada", "Cancelada"),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_OPCIONES, default="activa")

    def __str__(self):
        return f"{self.nombre} - Profesor: {self.clase_profesor.username}"