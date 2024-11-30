import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count

from estadio.models import Clase, Usuario


def listar_clases(request):
    clases = Clase.objects.annotate(
        total_usuarios=Count('clase_usuarios', distinct=True)  # Cambiado a 'clase_usuarios'
    ).values(
        'id',
        'clase_profesor__id',
        'clase_profesor__first_name', 
        'clase_profesor__last_name', 
        'total_usuarios',  # Cambiado a total_usuarios
        'nombre', 
        'descripcion', 
        'cupo_total', 
        'cupo_disponible'
    )
    return JsonResponse(list(clases), safe=False, status=200)

@csrf_exempt
def crear_clases(request):
    if request.method == 'POST':
        try:        
            data = json.loads(request.body)
            
            profesor = data.get('profesor')
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')
            cupo_total = data.get('cupo_total')
            
            usuarios_ids = []  # IDs de los usuarios que deseas añadir a la clase
            
            profesor = Usuario.objects.get(id=profesor)
            
            clase = Clase.objects.create(
                clase_profesor=profesor,
                nombre=nombre,
                descripcion=descripcion,
                cupo_total=cupo_total,
                cupo_disponible=cupo_total
            )
            
            if usuarios_ids:
                usuarios = Usuario.objects.filter(id__in=usuarios_ids)
                clase.usuarios.set(usuarios)
            
            clase.save()
            print(f'Clase creada: {clase}')
            return JsonResponse(clase.nombre, status=200, safe=False)
        
        except Exception as e:
            print(f'Error al crear la clase: {e}')
            return JsonResponse({'error': 'Error al crear la clase'}, status=400)
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def modificar_clase(request):
    if request.method == 'PUT':
        id = request.GET.get('id')
        
        try:
            data = json.loads(request.body)
            
            profesor = data.get('profesor')
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')
            cupo_total = data.get('cupo_total')
            
            print(f'Data: {data}')
                        
            profesor = Usuario.objects.get(id=11)
            
            clase = Clase.objects.get(id=id)
            clase.clase_profesor = profesor
            clase.nombre = nombre
            clase.descripcion = descripcion
            clase.cupo_total = cupo_total
            clase.save()
            print(f'Clase modificada: {clase}')
            return JsonResponse(clase.nombre, status=200, safe=False)
            
        except:
            return JsonResponse({'error': 'Clase no encontrada'}, status=404)
       
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def eliminar_clase(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        
        print(f'ID: {id}')
        
        try:
            clase = Clase.objects.get(pk=id)
            clase.delete()
            print(f'Clase eliminada: {clase}')
            return JsonResponse(clase.nombre, status=200, safe=False)
            
        except:
            return JsonResponse({'error': 'Clase no encontrada'}, status=404)
       
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

def profesores_disponibles(request):
    profesores = Usuario.objects.filter(rol=2)
    print(f'Profesores disponibles: {profesores}')
    return JsonResponse(list(profesores.values('id', 'first_name', 'last_name')), safe=False, status=200)

def alumnos_con_estado(request):
    id_clase = request.GET.get('clase_id')

    try:
        # Obtener alumnos en clase
        alumnos_en_clase = Clase.objects.get(id=id_clase).clase_usuarios.values('id', 'first_name', 'last_name')
        
        # Obtener alumnos disponibles (rol=3 y no en la clase)
        alumnos_disponibles = Usuario.objects.filter(rol=3).exclude(id__in=[alumno['id'] for alumno in alumnos_en_clase]).values('id', 'first_name', 'last_name')
        
        # Agregar un estado a cada alumno
        alumnos_con_estado = [{'id': alumno['id'], 'first_name': alumno['first_name'], 'last_name': alumno['last_name'], 'estado': 2} for alumno in alumnos_en_clase]
        alumnos_con_estado += [{'id': alumno['id'], 'first_name': alumno['first_name'], 'last_name': alumno['last_name'], 'estado': 1} for alumno in alumnos_disponibles]

        return JsonResponse(alumnos_con_estado, safe=False, status=200)
    
    except Clase.DoesNotExist:
        return JsonResponse({'error': 'Clase no encontrada'}, status=404)
    
@csrf_exempt
def añadir_alumnos(request):
    if request.method == 'POST':
        try:
            id_clase = request.GET.get('clase_id')
            if not id_clase:
                return JsonResponse({'error': 'ID de clase no proporcionado'}, status=400)

            data = json.loads(request.body)
            alumnos_ids = data.get('alumnos')
            if not isinstance(alumnos_ids, list):
                return JsonResponse({'error': 'Formato de alumnos inválido'}, status=400)

            clase = Clase.objects.get(id=id_clase)

            clase.clase_usuarios.set(alumnos_ids)  # Reemplaza todos los alumnos de la clase
            return JsonResponse({'message': 'Alumnos sincronizados correctamente'}, status=200)
        
        except Clase.DoesNotExist:
            return JsonResponse({'error': 'Clase no encontrada'}, status=404)
        except Exception as e:
            print(f'Error al sincronizar alumnos: {e}')
            return JsonResponse({'error': 'Error al sincronizar alumnos'}, status=400)
        
    return JsonResponse({'error': 'Método no permitido'}, status=405)