from django.db import models

from .Reserva import Reserva
from .Inventario import Inventario

class ReservaEquipamiento(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='equipamientos_reservados')
    equipamiento = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    devuelto_en_buen_estado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reserva de {self.cantidad} {self.equipamiento.nombre} para la reserva {self.reserva}"