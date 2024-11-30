from django.db.models import Count
from django.http import JsonResponse

from estadio.models import Clase, Mantenimiento, Reserva
from estadio.models.Cancha import Cancha
from estadio.models.Usuario import Usuario


def resumen_general(request):
    try:
        total_reservas = Reserva.objects.count()
        total_usuarios = Usuario.objects.count()
        total_canchas = Cancha.objects.count()
        total_clases = Clase.objects.count()
        clases_con_usuarios = Clase.objects.annotate(
            num_usuarios=Count("clase_usuarios", distinct=True)
        )
        total_usuarios_en_clases = sum(
            clase.num_usuarios for clase in clases_con_usuarios
        )
        promedio_alumnos_por_clase = (
            total_usuarios_en_clases / total_clases if total_clases else 0
        )
        total_alumnos = Usuario.objects.filter(rol__nombre="Usuario").count()
        reservas_confirmadas = Reserva.objects.filter(estado="Confirmada").count()
        reservas_canceladas = Reserva.objects.filter(estado="Cancelada").count()
        reservas_pendientes = Reserva.objects.filter(estado="Pendiente").count()
        usuarios_tipo = {
            "personal": Usuario.objects.filter(rol__nombre="Personal").count(),
            "admin": Usuario.objects.filter(rol__nombre="Administrador").count(),
            "profesor": Usuario.objects.filter(rol__nombre="Profesor").count(),
        }
        resumen_data = {
            "totalReservas": total_reservas,
            "totalUsuarios": total_usuarios,
            "totalCanchas": total_canchas,
            "totalClases": total_clases,
            "promedioAlumnosPorClase": promedio_alumnos_por_clase,
            "totalAlumnos": total_alumnos,
            "totalTorneos": 0,
            "reservasConfirmadas": reservas_confirmadas,
            "reservasCanceladas": reservas_canceladas,
            "reservasPendientes": reservas_pendientes,
            "usuariosTipo": usuarios_tipo,
        }

        return JsonResponse(resumen_data, status=200)
    except Exception as e:
        print(f"Error: {str(e)}")  # Para ver el error exacto
        return JsonResponse({"error": str(e)}, status=500)

def reservas_por_usuario(request):
    try:
        reservas = (
            Reserva.objects.filter(estado='confirmada').values("usuario__username")  # Agrupamos por usuario
            .annotate(total_reservas=Count("id"))  # Contamos las reservas por usuario
            .order_by("-total_reservas")  # Ordenamos por más reservas
        )

        return JsonResponse(list(reservas), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def uso_canchas_subcanchas(request):
    try:
        reservas = Reserva.objects.filter(estado='confirmada')

        # Contabilizar uso de canchas sin subcancha asociada
        uso_canchas = reservas.filter(subcancha__isnull=True).values('cancha__nombre', 'fecha').annotate(
            cantidad_uso=Count('cancha')
        ).order_by('fecha')

        # Contabilizar uso de subcanchas
        uso_subcanchas = reservas.filter(subcancha__isnull=False).values('subcancha__nombre', 'fecha').annotate(
            cantidad_uso=Count('subcancha')
        ).order_by('fecha')

        # Estructura de datos para las respuestas
        data = {
            "canchas": [],
            "subcanchas": []
        }

        # Organizar los datos de canchas
        for item in uso_canchas:
            if item['cantidad_uso'] > 0:  # Excluir si la cantidad_uso es 0
                data["canchas"].append({
                    'cancha': item['cancha__nombre'],
                    'cantidad_uso': item['cantidad_uso'],
                    'fecha': item['fecha']
                })

        # Organizar los datos de subcanchas
        for item in uso_subcanchas:
            if item['cantidad_uso'] > 0:  # Excluir si la cantidad_uso es 0
                data["subcanchas"].append({
                    'subcancha': item['subcancha__nombre'],
                    'cantidad_uso': item['cantidad_uso'],
                    'fecha': item['fecha']
                })

        # Devolver el JSON con los datos
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def mantenimiento(request):
    try:
        # Contabilizar mantenimientos solo para las canchas (sin subcancha)
        canchas_mantenimiento = Mantenimiento.objects.filter(subcancha__isnull=True) \
            .values('cancha__nombre') \
            .annotate(num_mantenimientos=Count('id'))

        # Contabilizar mantenimientos para las subcanchas (con subcancha)
        subcanchas_mantenimiento = Mantenimiento.objects.filter(subcancha__isnull=False) \
            .values('cancha__nombre', 'subcancha__nombre') \
            .annotate(num_mantenimientos=Count('id'))

        # Formatear los datos de las canchas (sin subcancha)
        canchas_data = [
            {
                'cancha': m['cancha__nombre'],
                'subcancha': 'N/A',  # No hay subcancha
                'num_mantenimientos': m['num_mantenimientos'],
            }
            for m in canchas_mantenimiento
        ]

        # Formatear los datos de las subcanchas
        subcanchas_data = [
            {
                'cancha': m['cancha__nombre'],
                'subcancha': m['subcancha__nombre'],
                'num_mantenimientos': m['num_mantenimientos'],
            }
            for m in subcanchas_mantenimiento
        ]

        # Combinar los resultados
        data = canchas_data + subcanchas_data
        
        # Respuesta en formato JSON
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def clases(requets):
    try:
        activas = Clase.objects.filter(estado="activa").count()
        completadas = Clase.objects.filter(estado="completada").count()
        canceladas = Clase.objects.filter(estado="cancelada").count()

        estudiantesPorClase = Clase.objects.annotate(
            estudiantes=Count("clase_usuarios")
        ).values("nombre", "estudiantes")
        
        data = {
            "activas": activas,
            "completadas": completadas,
            "canceladas": canceladas,
            "estudiantesPorClase": list(estudiantesPorClase),
        }

        print(data)

        return JsonResponse(data, status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)