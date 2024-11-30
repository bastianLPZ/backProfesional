from django.db import models

class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad_subcanchas = models.IntegerField(default=0)  # Número de subcanchas si tiene
    largo = models.DecimalField(max_digits=5, decimal_places=2)  # Tamaño en metros
    ancho = models.DecimalField(max_digits=5, decimal_places=2)  # Tamaño en metros
    ubicacion_x = models.DecimalField(max_digits=10, decimal_places=2)  # Coordenada X
    ubicacion_y = models.DecimalField(max_digits=10, decimal_places=2)  # Coordenada Y

    def __str__(self):
        return self.nombre