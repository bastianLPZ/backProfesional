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
    
def unirse_clase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_clase = data.get('id_clase')
            id_usuario = data.get('id_usuario')
            
            clase = Clase.objects.get(id=id_clase)
            usuario = Usuario.objects.get(id=id_usuario)
            
            if clase.cupo_disponible > 0:
                clase.cupo_disponible -= 1
                clase.save()
                
                usuario.clases.add(clase)
                usuario.save()
                
                return JsonResponse({'message': 'Usuario inscrito correctamente'}, safe=False, status=200)
            else:
                return JsonResponse({'message': 'No hay cupos disponibles'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)