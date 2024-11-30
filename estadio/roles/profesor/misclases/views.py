import json
from django.http import JsonResponse
from estadio.models import Clase, Usuario
from django.views.decorators.csrf import csrf_exempt

def list_class(request):
    clases = Clase.objects.all()
    clases_list = list(clases.values('id', 'nombre', 'descripcion', 'cupo_total', 'cupo_disponible'))
    return JsonResponse(clases_list, safe=False, status=200)

@csrf_exempt
def crear_class(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Obtener los datos del cuerpo de la solicitud
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')
            cupo_total = data.get('cupos')

            # Validar que los campos no estén vacíos
            if not nombre or not descripcion or not cupo_total:
                return JsonResponse({'message': 'Faltan campos requeridos'}, status=400)

            # Convertir 'cupos' a entero
            try:
                cupo_total = int(cupo_total)
            except ValueError:
                return JsonResponse({'message': 'El valor de "cupos" debe ser un número entero'}, status=400)

            print(f'Data: {data}')
            
            usuario = Usuario.objects.get(id=27)

            # Crear la clase
            clase = Clase.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                cupo_total=cupo_total,
                cupo_disponible=cupo_total,
                clase_profesor=usuario
            )
            clase.save()

            return JsonResponse({'message': 'Clase creada correctamente'}, safe=False, status=200)

        except Exception as e:
            # Captura de excepciones generales
            print(f"Error: {e}")
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
def editar_clase(request):
    
    id_clase = request.GET.get('id')
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            nombre = data.get('nombre')
            descripcion = data.get('descripcion')

            if not nombre or not descripcion:
                return JsonResponse({'message': 'Faltan campos requeridos'}, status=400)

            # Buscar la clase por su ID
            clase = Clase.objects.get(id=id_clase)

            # Actualizar los datos de la clase
            clase.nombre = nombre
            clase.descripcion = descripcion
            clase.save()

            return JsonResponse({'message': 'Clase actualizada correctamente'}, safe=False, status=200)

        except Exception as e:
            # Captura de excepciones generales
            print(f"Error: {e}")
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
@csrf_exempt
def eliminar_clase(request):
    id_clase = request.GET.get('id')
    
    if request.method == 'DELETE':
        try:

            if not id_clase:
                return JsonResponse({'message': 'Faltan campos requeridos'}, status=400)

            clase = Clase.objects.get(id=id_clase)

            clase.delete()

            return JsonResponse({'message': 'Clase eliminada correctamente'}, safe=False, status=200)

        except Exception as e:
            # Captura de excepciones generales
            print(f"Error: {e}")
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
def listar_estudiantes(request):
    id_profe = request.GET.get('id')
    
    profesor = Usuario.objects.filter(pk=id_profe)
    
    
