import json
from django.db.models import Count
from datetime import date, timedelta
import datetime
from django.http import JsonResponse
from django.db.models import F

from estadio.models import Clase, Usuario, Reserva


def dashboard_metrics(request):
    user_data = request.GET.get('user')

    user_dict = json.loads(user_data) if user_data else {}

    user_id = user_dict.get('id')

    if user_id:
        usuario = Usuario.objects.get(id=user_id)
    else:
        print("Invalid user id")
        
    clases_activas = Clase.objects.filter(
        estado="activa", clase_profesor=usuario
    ).count()

    estudiantes_registrados = (
        Usuario.objects.filter(
            rol__nombre="usuario",  # Usuarios con rol de "usuario"
            clase_usuarios__clase_profesor=usuario,  # Usuarios en clases cuyo profesor es el usuario actual
        )
        .distinct()
        .count()
    )

    reservas_proximas = Reserva.objects.filter(
        estado="confirmada", usuario=usuario, fecha__gte=datetime.date.today()
    ).count()

    estudiantes_en_clases = (
        Clase.objects.filter(clase_profesor=usuario, estado="activa").aggregate(
            total_estudiantes=Count("clase_usuarios")
        )["total_estudiantes"]
        or 0
    )

    # Preparar los datos de respuesta
    data = {
        "clases_activas": clases_activas,
        "estudiantes_registrados": estudiantes_registrados,
        "reservas_proximas": reservas_proximas,
        "estudiantes_en_clases": estudiantes_en_clases,
    }

    return JsonResponse(data)

def progreso_cupos_clases(request):
    # Obtener el ID del usuario directamente de la URL
    user_id = request.GET.get('user')

    # Verifica si se obtuvo un user_id y si es válido
    if user_id is not None:
        try:
            usuario = Usuario.objects.get(id=user_id)  # Buscar al usuario por ID
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    else:
        return JsonResponse({"error": "ID de usuario no proporcionado"}, status=400)

    clases = list(
        Clase.objects.filter(clase_profesor=usuario, estado="activa")
        .annotate(cupos_ocupados=F("cupo_total") - F("cupo_disponible"))
        .values("nombre", "cupos_ocupados", "cupo_total", 'cupo_disponible')
    )

    return JsonResponse(clases, safe=False, status=200)