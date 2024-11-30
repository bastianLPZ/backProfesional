from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from .Rol import Rol

class Usuario(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='usuarios', null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(Group, related_name='usuarios_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='usuarios_permissions', blank=True)

    def __str__(self):
        return f"{self.username} ({self.rol.nombre if self.rol else 'Sin rol'})"