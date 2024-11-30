import json
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from estadio.models import Mantenimiento
from estadio.models.Cancha import Cancha
from estadio.models.Subcancha import Subcancha
from estadio.models.Usuario import Usuario


def listar_mantenimientos(request):
    mantenimientos = Mantenimiento.objects.all().values(
        'id',
        'cancha__id',
        'cancha__nombre',
        'subcancha__id',
        'subcancha__nombre',
        'fecha',
        'tipo',
        'comentarios',
        'encargado__id',
        'encargado__first_name',
        'encargado__last_name'
    )
    return JsonResponse(list(mantenimientos), safe=False, status=200)

@csrf_exempt
def crear_mantenimiento(request):
    
    print('***CREAR MANTENIMIENTO***')
    
    if request.method == 'POST':
            
        try:
            
            body_unicode = request.body.decode('utf-8')  
            body_data = json.loads(body_unicode)  
            
            print(body_data)
                        
            fecha = body_data.get('fecha')
            tipo = body_data.get('tipo')
            comentarios = body_data.get('comentarios')
            
            cancha = body_data.get('cancha')
            encargado = body_data.get('encargado')
            subcancha = body_data.get('subcanchas')
                        
            cancha = Cancha.objects.get(pk=cancha)
                                
            encargado = Usuario.objects.get(pk=encargado)
            
            mantenimiento = Mantenimiento(
                cancha=cancha,
                fecha=fecha,
                tipo=tipo,
                comentarios=comentarios,
                encargado=encargado
            )
            
            if subcancha is not None:
                subcancha = Subcancha.objects.get(pk=subcancha)
                mantenimiento.subcancha = subcancha
            
            mantenimiento.save()
            
            return JsonResponse({'message': 'Mantenimiento creado'}, status=201)
            
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def editar_mantenimiento(request):
    if request.method == 'PUT':
        id = request.GET.get('id')
        
        try:
            
            body_unicode = request.body.decode('utf-8')  
            body_data = json.loads(body_unicode)  
            
            fecha = body_data.get('fecha')
            tipo = body_data.get('tipo')
            comentarios = body_data.get('comentarios')
            
            mantenimiento = Mantenimiento.objects.get(id=id)
            
            mantenimiento.fecha = fecha
            mantenimiento.tipo = tipo
            mantenimiento.comentarios = comentarios
            
            mantenimiento.save()
            
            return JsonResponse({'message': 'Mantenimiento actualizado'}, status=200)
            
        except Mantenimiento.DoesNotExist:
            return JsonResponse({'message': 'Mantenimiento no encontrado'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=500)
        
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
def eliminar_mantenimiento(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        
        try:
            mantenimiento = Mantenimiento.objects.get(id=id)
            mantenimiento.delete()
            return JsonResponse({'message': 'Mantenimiento eliminado'}, status=200)
        except Mantenimiento.DoesNotExist:
            return JsonResponse({'message': 'Mantenimiento no encontrado'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=500)