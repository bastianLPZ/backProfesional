from django.db import models

class Inventario(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    cantidad_total = models.IntegerField(default=0)  # Cantidad total en inventario
    cantidad_disponible = models.IntegerField(default=0)  # Cantidad disponible para reservas
    estado = models.CharField(max_length=50, choices=[('disponible', 'Disponible'), ('en mantenimiento', 'En mantenimiento'), ('desechado', 'Desechado')])

    def __str__(self):
        return f"{self.nombre} - {self.estado} ({self.cantidad_disponible}/{self.cantidad_total} disponibles)"