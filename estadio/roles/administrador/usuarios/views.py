import json
from django.http import JsonResponse
from estadio.models.Usuario import Usuario
from estadio.models.Rol import Rol
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

#############################
######ADMINISTRADORES########
#############################
def listar_administradores(request):
    try:
        administradores = Usuario.objects.filter(rol__nombre='Administrador')
    except Usuario.DoesNotExist:
        administradores = None
    return JsonResponse(list(administradores.values()), safe=False, status=200)

@csrf_exempt
def crear_administrador(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)
            nombre=data.get('first_name')
            apellido=data.get('last_name')
            correo=data.get('email')
            telefono=data.get('telefono')
            direccion=data.get('direccion')
            username=data.get('username')
            password=data.get('password')
            
            print(f'Data: {data}')
            
            rol = Rol.objects.get(nombre='Administrador')
            
            usuario = Usuario.objects.create(
                username=username,
                first_name=nombre,
                last_name=apellido,
                email=correo,
                telefono=telefono,
                direccion=direccion,
                rol=rol,
                password=make_password(password)
            )
            print(f'Usuario creado: {usuario}')
            return JsonResponse({'usuario': usuario.username}, status=201)
        
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def editar_administrador(request):
    if request.method == 'PUT':
        id = request.GET.get('id')
        try:
            data=json.loads(request.body)
            first_name=data.get('first_name')
            last_name=data.get('last_name')
            username=data.get('username')
            email=data.get('email')
            telefono=data.get('telefono')
            direccion=data.get('direccion')
            
            print(f'Data: {data}')
            
            usuario = Usuario.objects.get(id=id)
            
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.email = email
            usuario.telefono = telefono
            usuario.direccion = direccion
            usuario.username = username
            usuario.save()
            return JsonResponse({'usuario': usuario.username}, status=200)
        
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def eliminar_administrador(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()
            return JsonResponse({'usuario': usuario.username}, status=200)
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

#############################
#########PROFESORES##########
#############################
def listar_profesores(request):
    try:
        profesores = Usuario.objects.filter(rol__nombre='Profesor')
    except Usuario.DoesNotExist:
        profesores = None
    return JsonResponse(list(profesores.values()), safe=False, status=200)

@csrf_exempt
def crear_profesor(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)
            nombre=data.get('first_name')
            apellido=data.get('last_name')
            correo=data.get('email')
            telefono=data.get('telefono')
            direccion=data.get('direccion')
            username=data.get('username')
            password=data.get('password')
            
            print(f'Data: {data}')
            
            rol = Rol.objects.get(nombre='Profesor')
            
            usuario = Usuario.objects.create(
                username=username,
                first_name=nombre,
                last_name=apellido,
                email=correo,
                telefono=telefono,
                direccion=direccion,
                rol=rol,
                password=make_password(password)
            )
            print(f'Usuario creado: {usuario}')
            return JsonResponse({'usuario': usuario.username}, status=201)
        
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def editar_profesor(request):
    if request.method == 'PUT':
        id = request.GET.get('id')
        try:
            data=json.loads(request.body)
            first_name=data.get('first_name')
            last_name=data.get('last_name')
            username=data.get('username')
            email=data.get('email')
            telefono=data.get('telefono')
            direccion=data.get('direccion')
            
            print(f'Data: {data}')
            
            usuario = Usuario.objects.get(id=id)
            
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.email = email
            usuario.telefono = telefono
            usuario.direccion = direccion
            usuario.username = username
            usuario.save()
            return JsonResponse({'usuario': usuario.username}, status=200)
        
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def eliminar_profesor(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()
            return JsonResponse({'usuario': usuario.username}, status=200)
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

#############################
##########USUARIOS###########
#############################
def listar_usuarios(request):
    try:
        usuarios = Usuario.objects.filter(rol__nombre='Usuario')
    except Usuario.DoesNotExist:
        usuarios = None
    return JsonResponse(list(usuarios.values()), safe=False, status=200)

@csrf_exempt
def crear_usuario(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)
            nombre=data.get('first_name')
            apellido=data.get('last_name')
            correo=data.get('email')
            telefono=data.get('telefono')
            direccion=data.get('direccion')
            username=data.get('username')
            password=data.get('password')
            
            print(f'Data: {data}')
            
            rol = Rol.objects.get(nombre='Usuario')
            
            usuario = Usuario.objects.create(
                username=username,
                first_name=nombre,
                last_name=apellido,
                email=correo,
                telefono=telefono,
                direccion=direccion,
                rol=rol,
                password=make_password(password)
            )
            print(f'Usuario creado: {usuario}')
            return JsonResponse({'usuario': usuario.username}, status=201)
        
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def editar_usuario(request):
    if request.method == 'PUT':
        id = request.GET.get('id')
        try:
            data=json.loads(request.body)
            first_name=data.get('first_name')
            last_name=data.get('last_name')
            username=data.get('username')
            email=data.get('email')
            telefono=data.get('telefono')
            direccion=data.get('direccion')
            
            print(f'Data: {data}')
            
            usuario = Usuario.objects.get(id=id)
            
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.email = email
            usuario.telefono = telefono
            usuario.direccion = direccion
            usuario.username = username
            usuario.save()
            return JsonResponse({'usuario': usuario.username}, status=200)
        
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def eliminar_usuario(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()
            return JsonResponse({'usuario': usuario.username}, status=200)
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

#############################
##########PERSONAL###########
#############################
def listar_personal(request):
    try:
        personal = Usuario.objects.filter(rol__nombre='Personal')
    except Usuario.DoesNotExist:
        personal = None
    return JsonResponse(list(personal.values()), safe=False, status=200)

@csrf_exempt
def crear_personal(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)
            nombre=data.get('first_name')
            apellido=data.get('last_name')
            correo=data.get('email')
            telefono=data.get('telefono')
            direccion=data.get('direccion')
            username=data.get('username')
            password=data.get('password')
            
            print(f'Data: {data}')
            
            rol = Rol.objects.get(nombre='Personal')
            
            usuario = Usuario.objects.create(
                username=username,
                first_name=nombre,
                last_name=apellido,
                email=correo,
                telefono=telefono,
                direccion=direccion,
                rol=rol,
                password=make_password(password)
            )
            print(f'Usuario creado: {usuario}')
            return JsonResponse({'usuario': usuario.username}, status=201)
        
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def editar_personal(request):
    if request.method == 'PUT':
        id = request.GET.get('id')
        try:
            data=json.loads(request.body)
            first_name=data.get('first_name')
            last_name=data.get('last_name')
            username=data.get('username')
            email=data.get('email')
            telefono=data.get('telefono')
            direccion=data.get('direccion')
            
            print(f'Data: {data}')
            
            usuario = Usuario.objects.get(id=id)
            
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.email = email
            usuario.telefono = telefono
            usuario.direccion = direccion
            usuario.username = username
            usuario.save()
            return JsonResponse({'usuario': usuario.username}, status=200)
        
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def eliminar_personal(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()
            return JsonResponse({'usuario': usuario.username}, status=200)
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)