import json
from django.http import JsonResponse
from estadio.models import Clase, Usuario, Rol
from django.views.decorators.csrf import csrf_exempt


def crear_usuario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f'Data: {data}')
            rolInstance = Rol.objects.get(id=data.get('rol'))
            user = Usuario.objects.create(
                
                email=data.get('email'),
                username=data.get('username'),
                password=data.get('password'),
                rol=rolInstance
            )
            
            user.save()
            
            return JsonResponse({'message': 'Usuario creado correctamente'}, safe=False, status=200)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({f'message': 'Error al crear usuario. El error es:'}, status=400)
            
    