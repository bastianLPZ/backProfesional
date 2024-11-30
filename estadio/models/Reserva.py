from django.db import models

from .Usuario import Usuario
from .Cancha import Cancha
from .Subcancha import Subcancha 
from .Inventario import Inventario

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cancha = models.ForeignKey(Cancha, null=True, blank=True, on_delete=models.CASCADE)
    subcancha = models.ForeignKey(Subcancha, null=True, blank=True, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')])
    equipamiento_reservado = models.ManyToManyField(Inventario, through='ReservaEquipamiento')

    def __str__(self):
        return f"Reserva de {self.usuario} en {self.cancha or self.subcancha} ({self.fecha})"