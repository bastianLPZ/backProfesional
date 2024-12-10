import json
from django.http import JsonResponse
from estadio.models import Clase, Usuario, Rol
from django.views.decorators.csrf import csrf_exempt


def listar_clases_disponibles(request):
    if request.method == 'GET':
        clases = Clase.objects.all()
        clases_list = list(clases.values('id', 'nombre', 'descripcion', 'cupo_total', 'cupo_disponible'))
        return JsonResponse(clases_list, safe=False, status=200)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
@csrf_exempt
def unirse_clase(request):
    if request.method == 'POST':
        try:
            # Cargar el cuerpo de la solicitud
            data = json.loads(request.body)
            print("Datos recibidos:", data)

            # Extraer IDs
            id_clase = data.get('id_clase')
            id_usuario = data.get('id_usuario')

            # Obtener la clase y el usuario
            clase = Clase.objects.get(id=id_clase)
            usuario = Usuario.objects.get(id=id_usuario)

            # Validar disponibilidad de cupo
            if clase.cupo_disponible > 0:
                clase.clase_usuarios.add(usuario)  # Agregar al Many-to-Many
                clase.cupo_disponible -= 1  # Reducir cupos disponibles
                clase.save()  # Guardar cambios en la clase

                return JsonResponse({'message': 'Usuario inscrito correctamente'}, safe=False, status=200)
            else:
                return JsonResponse({'message': 'No hay cupos disponibles'}, status=400)
        except Clase.DoesNotExist:
            return JsonResponse({'message': 'Clase no encontrada'}, status=404)
        except Usuario.DoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
@csrf_exempt
def salir_clase(request):
    if request.method == 'POST':  # Cambiado a POST por limitaciones del cuerpo en DELETE
        try:
            # Extraer datos del cuerpo de la solicitud
            data = json.loads(request.body)
            id_clase = data.get('id_clase')
            id_usuario = data.get('id_usuario')

            # Obtener la clase y el usuario
            clase = Clase.objects.get(id=id_clase)
            usuario = Usuario.objects.get(id=id_usuario)

            # Verificar si el usuario está inscrito en la clase
            if clase.clase_usuarios.filter(id=usuario.id).exists():
                # Aumentar el cupo disponible
                clase.cupo_disponible += 1
                clase.save()

                # Remover al usuario de la clase
                clase.clase_usuarios.remove(usuario)

                return JsonResponse({'message': 'Usuario eliminado correctamente'}, safe=False, status=200)
            else:
                return JsonResponse({'message': 'Usuario no inscrito en la clase'}, status=400)

        except Clase.DoesNotExist:
            return JsonResponse({'message': 'Clase no encontrada'}, status=404)
        except Usuario.DoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)