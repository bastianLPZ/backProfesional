from django.contrib import admin
from estadio.models import Cancha, Inventario, Mantenimiento, Reserva, ReservaEquipamiento, Rol, Subcancha, Usuario
from estadio.models import Clase

# Register your models here.
admin.site.register(Cancha)
admin.site.register(Inventario)
admin.site.register(Mantenimiento)
admin.site.register(Reserva)
admin.site.register(ReservaEquipamiento)
admin.site.register(Rol)
admin.site.register(Subcancha)
admin.site.register(Usuario)
admin.site.register(Clase)
