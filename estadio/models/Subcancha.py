from django.db import models

from .Cancha import Cancha

class Subcancha(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='subcanchas')
    nombre = models.CharField(max_length=100)
    largo = models.DecimalField(max_digits=5, decimal_places=2)  # Tamaño en metros
    ancho = models.DecimalField(max_digits=5, decimal_places=2)  # Tamaño en metros
    ubicacion_x = models.DecimalField(max_digits=10, decimal_places=2)  # Coordenada X dentro de la cancha
    ubicacion_y = models.DecimalField(max_digits=10, decimal_places=2)  # Coordenada Y dentro de la cancha

    def __str__(self):
        return f"Subcancha {self.nombre} de {self.cancha.nombre}"