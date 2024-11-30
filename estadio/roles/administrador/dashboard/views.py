from django.http import JsonResponse
from estadio.models.Usuario import Usuario
from estadio.models.Reserva import Reserva
from estadio.models.Cancha import Cancha
from estadio.models.Subcancha import Subcancha

def total_usuarios(request):
    try:
        print('---Contador usuarios---')
        
        total_usuarios = Usuario.objects.count()
        
        print(f'Total: {total_usuarios}')
        
        print('Consulta exitosa')
        return JsonResponse(total_usuarios, status=200, safe=False)
    except Exception as e:
        print(f'Error: {str(e)}')
        return JsonResponse({'error':str(e)})
    
def total_reservas(request):
    try:
        print('---Contador reservas---')
        
        total_reservas = Reserva.objects.count()
        
        print(f'Total: {total_reservas}')
        
        print('Consulta exitosa')
        return JsonResponse(total_reservas, status=200, safe=False)
    except Exception as e:
        print(f'Error: {str(e)}')
        return JsonResponse({'error':str(e)})
    
def canchas_disponibles(request):
    try:
        print('---Contador canchas---')
        
        canchas_disponibles = Cancha.objects.count()
        subcanchas_disponibles = Subcancha.objects.count()
        
        disponibles = canchas_disponibles + subcanchas_disponibles
        
        print(f'Total: {disponibles}')
        
        print('Consulta exitosa')
        return JsonResponse(disponibles, status=200, safe=False)
    except Exception as e:
        print(f'Error: {str(e)}')
        return JsonResponse({'error':str(e)})
    
def reservas_canceladas(request):
    try:
        print('---Contador reservas canceladas---')
        
        reservas_canceladas = Reserva.objects.filter(estado='cancelada').count()
        
        print(f'Total: {reservas_canceladas}')
        
        print('Consulta exitosa')
        return JsonResponse(reservas_canceladas, status=200, safe=False)
    except Exception as e:
        print(f'Error: {str(e)}')
        return JsonResponse({'error':str(e)})

def listar_canchas(request):
    try:
        print('---Listar canchas---')
        
        canchas = list(Cancha.objects.all().values('id', 'nombre', 'ancho', 'largo'))  # Convertir a lista
        
        print('Consulta exitosa')
        return JsonResponse(canchas, status=200, safe=False)
    except Exception as e:
        print(f'Error: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)
    
def info_cancha(request):
    try:
        print('---Info cancha---')
        id = request.GET.get('cancha')
        
        print(f'ID: {id}')

        # Obtiene la cancha principal
        cancha = Cancha.objects.get(pk=id)
        
        # Crea la estructura de respuesta
        cancha_info = {
            'nombre': cancha.nombre,
            'ancho': cancha.ancho,
            'largo': cancha.largo,
            'subcanchas': []
        }

        # Agrega las subcanchas a la respuesta
        for subcancha in cancha.subcanchas.all():
            subcancha_info = {
                'id': subcancha.id,
                'nombre': subcancha.nombre,
                'largo': subcancha.largo,
                'ancho': subcancha.ancho,
                'ubicacionX': subcancha.ubicacion_x,
                'ubicacionY': subcancha.ubicacion_y,
            }
            cancha_info['subcanchas'].append(subcancha_info)

        print('Consulta exitosa')
        print(cancha_info)
        return JsonResponse(cancha_info, status=200, safe=False)
    
    except Cancha.DoesNotExist:
        print(f'Error: Cancha con ID {id} no encontrada.')
        return JsonResponse({'error': 'Cancha no encontrada.'}, status=404)
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)