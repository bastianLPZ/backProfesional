from django.db import models

from .Cancha import Cancha
from .Subcancha import Subcancha
from .Usuario import Usuario

class Mantenimiento(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    subcancha = models.ForeignKey(Subcancha, null=True, blank=True, on_delete=models.CASCADE)
    fecha = models.DateField()
    tipo = models.CharField(max_length=100)
    comentarios = models.TextField(blank=True)
    encargado = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Mantenimiento de {self.cancha or self.subcancha} - {self.tipo} ({self.fecha})"