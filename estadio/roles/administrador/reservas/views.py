import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from estadio.models.Cancha import Cancha
from estadio.models.Reserva import Reserva
from estadio.models.Subcancha import Subcancha
from estadio.models.Usuario import Usuario
from estadio.models.Inventario import Inventario
from estadio.models.ReservaEquipamiento import ReservaEquipamiento
from django.db.models import Count, F
import traceback

#############################
##########CANCHAS############
#############################
@csrf_exempt
def crear_cancha(request):
    if request.method == 'POST':
        try:
            # Obtener datos de la solicitud
            data = json.loads(request.body)  # Cambiado para obtener el body
            nombre = data.get('nombre')
            subcancha = data.get('subcanchas')
            largo = data.get('largo')
            ancho = data.get('ancho')
            
            print(f'Data: {data}')

            # Crear la cancha
            cancha = Cancha.objects.create(
                nombre=nombre,
                capacidad_subcanchas=subcancha,
                largo=largo,
                ancho=ancho,
                ubicacion_x=0,
                ubicacion_y=0
            )
            print(f'Cancha creada: {cancha}')

            return JsonResponse({'message': 'Cancha y subcanchas creadas exitosamente'}, status=201)

        except Exception as e:
            print(f'Error al crear cancha: {e}')
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)

def listar_canchas(request):
    try:
        canchas = Cancha.objects.all().values('id', 'nombre', 'capacidad_subcanchas', 'largo', 'ancho')  # Obtener solo los campos necesarios
        canchas_list = list(canchas)  # Convertir a lista
        print(canchas_list)
        return JsonResponse(canchas_list, safe=False, status=200)  # Devolver los datos como JSON
    except Exception as e:
        print(f"Error al listar canchas: {e}")  # Imprimir el error en el servidor
        return JsonResponse({'error': 'Error al listar canchas'}, status=500)
    
@csrf_exempt
def eliminar_cancha(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            cancha = Cancha.objects.get(pk=id)
            cancha.delete()
            return JsonResponse({'message': 'Cancha eliminada correctamente.'}, status=204)  # No Content
        except Cancha.DoesNotExist:
            return JsonResponse({'error': 'Cancha no encontrada.'}, status=404)  # Not Found
        except Exception as e:
            print(f'Error al eliminar la cancha: {e}')  # Log del error
            return JsonResponse({'error': 'Error al eliminar la cancha.'}, status=500)  # Internal Server Error
    else:
        return JsonResponse({'error': 'Método no permitido. Usa DELETE.'}, status=405)  # Method Not Allowed

@csrf_exempt
def editar_cancha(request):
    if request.method == 'PUT':
        # Obtener el ID de la cancha del cuerpo de la solicitud
        id = request.GET.get('id')
        try:
            body_unicode = request.body.decode('utf-8')  # Decodificar el cuerpo de la solicitud
            body_data = json.loads(body_unicode)  # Cargar el cuerpo como JSON
            nombre = body_data.get('nombre')
            subcanchas = body_data.get('subcanchas')
            largo = body_data.get('largo')
            ancho = body_data.get('ancho')
            
            # print(f'Body data: {body_data}')

            cancha = Cancha.objects.get(pk=id)  # Obtener la cancha por ID

            # Actualizar los campos de la cancha
            cancha.nombre = nombre
            cancha.capacidad_subcanchas = subcanchas
            cancha.largo = largo
            cancha.ancho = ancho
            cancha.save()  # Guardar los cambios en la base de datos

            return JsonResponse({'message': 'Cancha editada correctamente.'}, status=200)  # OK
        except Cancha.DoesNotExist:
            return JsonResponse({'error': 'Cancha no encontrada.'}, status=404)  # Not Found
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al decodificar el JSON.'}, status=400)  # Bad Request
        except Exception as e:
            print(f'Error al editar la cancha: {e}')  # Log del error
            return JsonResponse({'error': 'Error al editar la cancha.'}, status=500)  # Internal Server Error
    else:
        return JsonResponse({'error': 'Método no permitido. Usa PUT.'}, status=405)  # Method Not Allowed
  
#############################
########SUBCANCHAS###########
#############################    
def listar_subcanchas(request):
    try:
        subcanchas = Subcancha.objects.all().values('id', 'nombre', 'largo', 'ancho')  # Obtener solo los campos necesarios
        subcanchas_list = list(subcanchas)  # Convertir a lista
        print(subcanchas_list)
        return JsonResponse(subcanchas_list, safe=False, status=200)  # Devolver los datos como JSON
    except Exception as e:
        print(f"Error al listar subcanchas: {e}")  # Imprimir el error en el servidor
        return JsonResponse({'error': 'Error al listar subcanchas'}, status=500)
    
@csrf_exempt
def crear_subcancha(request):
    if request.method == 'POST':
        try:
            # Obtener datos de la solicitud
            data = json.loads(request.body)
            nombre = data.get('nombre')
            cancha_id = data.get('cancha')  # ID de la cancha
            orientacion = data.get('orientacion')

            print(f'Data: {data}')

            # Obtener la cancha por su ID
            cancha = Cancha.objects.get(pk=cancha_id)
            largo_cancha = cancha.largo
            ancho_cancha = cancha.ancho

            # Inicializar largo y ancho de la subcancha
            largo_subcancha = 0
            ancho_subcancha = 0
            ubicacion_x = 0
            ubicacion_y = 0

            # Calcular largo y ancho de la subcancha según la capacidad de la cancha
            if cancha.capacidad_subcanchas >= 4:
                largo_subcancha = largo_cancha / 2  # Dividir en 2 por la longitud
                ancho_subcancha = ancho_cancha / 2  # Dividir en 2 por el ancho

                # Asignar ubicaciones según la orientación
                if orientacion == "Norte Izquierda":
                    ubicacion_x = 0
                    ubicacion_y = 0
                elif orientacion == "Norte Derecha":
                    ubicacion_x = ancho_subcancha
                    ubicacion_y = 0
                elif orientacion == "Sur Izquierda":
                    ubicacion_x = 0
                    ubicacion_y = largo_subcancha
                elif orientacion == "Sur Derecha":
                    ubicacion_x = ancho_subcancha
                    ubicacion_y = largo_subcancha

            elif cancha.capacidad_subcanchas == 2:
                largo_subcancha = largo_cancha  # Mismo largo
                ancho_subcancha = ancho_cancha / 2  # Dividir por el ancho

                # Asignar ubicaciones según la orientación
                if orientacion == "Norte":
                    ubicacion_x = 0
                    ubicacion_y = 0
                elif orientacion == "Sur":
                    ubicacion_x = ancho_subcancha
                    ubicacion_y = 0

            # Crear la subcancha
            subcancha = Subcancha.objects.create(
                nombre=nombre,
                cancha=cancha,
                largo=largo_subcancha,
                ancho=ancho_subcancha,
                ubicacion_x=ubicacion_x,
                ubicacion_y=ubicacion_y
            )
            print(f'Subcancha creada: {subcancha}')

            return JsonResponse({'message': 'Subcancha creada exitosamente'}, status=200)

        except Exception as e:
            print(f'Error al crear subcancha: {e}')
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
def eliminar_subcancha(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            subcancha = Subcancha.objects.get(pk=id)
            subcancha.delete()
            return JsonResponse({'message': 'Subcancha eliminada correctamente.'}, status=204)  # No Content
        except Subcancha.DoesNotExist:
            return JsonResponse({'error': 'Subcancha no encontrada.'}, status=404)
        
        except Exception as e:
            print(f'Error al eliminar la subcancha: {e}')
            return JsonResponse({'error': 'Error al eliminar la subcancha.'}, status=500)
        
    else:
        return JsonResponse({'error': 'Método no permitido. Usa DELETE.'}, status=405)
    
@csrf_exempt
def editar_subcancha(request):
    if request.method == 'PUT':
        # Obtener el ID de la cancha del cuerpo de la solicitud
        id = request.GET.get('id')
        try:
            body_unicode = request.body.decode('utf-8')  # Decodificar el cuerpo de la solicitud
            body_data = json.loads(body_unicode)  # Cargar el cuerpo como JSON
            nombre = body_data.get('nombre')
            largo = body_data.get('largo')
            ancho = body_data.get('ancho')
            
            print(f'Body data: {body_data}')

            subcancha = Subcancha.objects.get(pk=id)  # Obtener la cancha por ID

            # Actualizar los campos de la cancha
            subcancha.nombre = nombre
            subcancha.largo = largo
            subcancha.ancho = ancho
            subcancha.save()  # Guardar los cambios en la base de datos

            return JsonResponse({'message': 'Subcancha editada correctamente.'}, status=200)  # OK
        except Subcancha.DoesNotExist:
            return JsonResponse({'error': 'Subcancha no encontrada.'}, status=404)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al decodificar el JSON.'}, status=400)
        
        except Exception as e:
            print(f'Error al editar la subcancha: {e}')
            return JsonResponse({'error': 'Error al editar la subcancha.'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido. Usa PUT.'}, status=405)
    
def canchas_disponibles(request):
    # print("Solicitud recibida para obtener canchas disponibles.")  # Indica que se ha recibido una solicitud
    try:
        # Filtrar canchas con capacidad de subcanchas > 0 y que no hayan alcanzado su capacidad máxima
        # print("Filtrando canchas con capacidad de subcanchas y capacidad máxima.")  # Indica que se está filtrando
        canchas = (
            Cancha.objects.annotate(subcanchas_count=Count('subcanchas'))  # Cuenta las subcanchas existentes para cada cancha
            .filter(capacidad_subcanchas__gt=0, subcanchas_count__lt=F('capacidad_subcanchas'))
            .values('id', 'nombre')  # Obtener solo los campos necesarios
        )
        
        canchas_list = list(canchas)  # Convertir a lista para JSON
        # print(f"Canchas disponibles encontradas: {canchas_list}")  # Muestra las canchas encontradas

        return JsonResponse(canchas_list, safe=False, status=200)  # Devolver los datos como JSON
    except Exception as e:
        print(f"Error al listar canchas: {e}")  # Imprimir el error en el servidor
        return JsonResponse({'error': 'Error al listar canchas'}, status=500)    

def orientaciones_disponibles(request):
    print("Solicitud recibida para obtener orientaciones de subcanchas disponibles.")  # Indica que se ha recibido una solicitud
    try:
        cancha_id = request.GET.get('cancha')
        
        print(f'Id recibido: {cancha_id}')
        # Obtener la cancha por su ID
        cancha = Cancha.objects.get(pk=cancha_id)
        print(f"Cancha obtenida: {cancha.nombre} con capacidad de subcanchas: {cancha.capacidad_subcanchas}")  # Imprime detalles de la cancha

        # Obtener las subcanchas que ya están creadas para esta cancha
        subcanchas_creadas = Subcancha.objects.filter(cancha=cancha).values('ubicacion_x', 'ubicacion_y')

        # Determinar las orientaciones ocupadas
        orientaciones_ocupadas = set()

        for subcancha in subcanchas_creadas:
            if cancha.capacidad_subcanchas >= 4:  # Si la cancha puede dividirse en 4
                if subcancha['ubicacion_x'] < (cancha.ancho / 2) and subcancha['ubicacion_y'] < (cancha.largo / 2):
                    orientaciones_ocupadas.add("Norte Izquierda")
                elif subcancha['ubicacion_x'] >= (cancha.ancho / 2) and subcancha['ubicacion_y'] < (cancha.largo / 2):
                    orientaciones_ocupadas.add("Norte Derecha")
                elif subcancha['ubicacion_x'] < (cancha.ancho / 2) and subcancha['ubicacion_y'] >= (cancha.largo / 2):
                    orientaciones_ocupadas.add("Sur Izquierda")
                elif subcancha['ubicacion_x'] >= (cancha.ancho / 2) and subcancha['ubicacion_y'] >= (cancha.largo / 2):
                    orientaciones_ocupadas.add("Sur Derecha")
            elif cancha.capacidad_subcanchas == 2:  # Si la cancha puede dividirse en 2
                if subcancha['ubicacion_x'] < (cancha.ancho / 2):
                    orientaciones_ocupadas.add("Norte")
                else:
                    orientaciones_ocupadas.add("Sur")

        # Definir las orientaciones posibles
        orientaciones_posibles = set()
        if cancha.capacidad_subcanchas >= 4:
            orientaciones_posibles = {"Norte Izquierda", "Norte Derecha", "Sur Izquierda", "Sur Derecha"}
        elif cancha.capacidad_subcanchas == 2:
            orientaciones_posibles = {"Izquierda", "Derecha"}

        # Calcular orientaciones disponibles restando las ocupadas de las posibles
        orientaciones_disponibles = list(orientaciones_posibles - orientaciones_ocupadas)
        print(f"Orientaciones disponibles encontradas: {orientaciones_disponibles}")  # Muestra las orientaciones encontradas

        return JsonResponse(orientaciones_disponibles, safe=False, status=200)  # Devolver los datos como JSON
    except Exception as e:
        print(f"Error al listar orientaciones de subcanchas: {e}")  # Imprimir el error en el servidor
        return JsonResponse({'error': 'Error al listar orientaciones de subcanchas'}, status=500)
    
#############################
###########HORAS#############
#############################    
def listar_horas(request):
    print(f'Solicitud recibida para obtener horas ocupadas.')
    try:
        reservas = Reserva.objects.all()
        
        lista_reservas = []

        for reserva in reservas:
            lista_reservas.append({
                'id': reserva.id,
                'usuario': reserva.usuario.username,  # Puedes acceder a otros campos de usuario si es necesario
                'cancha': reserva.cancha.nombre if reserva.cancha else None,
                'subcancha': reserva.subcancha.nombre if reserva.subcancha else None,
                'fecha': reserva.fecha,
                'hora_inicio': reserva.hora_inicio,
                'hora_fin': reserva.hora_fin,
                'estado': reserva.estado,
                'equipamiento_reservado': [equipamiento.nombre for equipamiento in reserva.equipamiento_reservado.all()]
            })
            
        return JsonResponse(lista_reservas, safe=False, status=200)
        
    except Exception as e:
        print(f'Error al listar horas ocupadas: {e}')
        return JsonResponse({'error': 'Error al listar horas ocupadas'}, status=500)
    
def estados_disponibles(request):
    # print("Solicitud recibida para obtener estados disponibles.")
    try:
        estados = Reserva._meta.get_field('estado').choices  # Obtener las opciones de estado
        estados_list = [estado[0] for estado in estados]  # Obtener solo los valores de estado
        # print(f"Estados disponibles: {estados_list}")  # Muestra los estados disponibles
        return JsonResponse(estados_list, safe=False, status=200)  # Devolver los datos como JSON
    except Exception as e:
        print(f"Error al listar estados: {e}")  # Imprimir el error en el servidor
        return JsonResponse({'error': 'Error al listar estados'}, status=500)  # Internal Server Error
    
def listar_canchas_disponibles(request):
    # print("Solicitud recibida para obtener canchas disponibles.")  # Indica que se ha recibido una solicitud
    try:
        cancha = Cancha.objects.all().values('id', 'nombre')  # Obtener solo los campos necesarios
        cancha_list = list(cancha)  # Convertir a lista para JSON
        # print(f"Canchas disponibles encontradas: {cancha_list}")  # Muestra las canchas encontradas
        return JsonResponse(cancha_list, safe=False, status=200)  # Devolver los datos como JSON
    except Exception as e:
        print(f"Error al listar canchas: {e}")
        return JsonResponse({'error': 'Error al listar canchas'}, status=500)

@csrf_exempt
def editar_reserva(request):
    if request.method == 'PUT':
        id = request.GET.get('id')
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            
            print(f'Body data: {body_data}')
            
            cancha = body_data.get('cancha')  # Ahora es el nombre de la cancha
            fecha = body_data.get('fecha')
            hora_inicio = body_data.get('horaInicio')
            hora_fin = body_data.get('horaFin')
            estado = body_data.get('estado')
            equipamientos_nombres = body_data.get('equipamientos', [])

            # Buscar la cancha por nombre
            # Verificar si 'cancha' es un ID numérico o un nombre
            if str(cancha).isdigit():
                # Si 'cancha' es un número, buscar por ID
                cancha = get_object_or_404(Cancha, pk=int(cancha))
            else:
                # Si 'cancha' es un nombre, buscar por nombre
                cancha = get_object_or_404(Cancha, nombre=cancha)

            reserva = get_object_or_404(Reserva, pk=id)

            # Verificar si hay una reserva confirmada en el mismo horario
            if estado == 'confirmada':
                conflictos_cancha = Reserva.objects.filter(
                    cancha=cancha,
                    fecha=fecha,
                    hora_inicio__lt=hora_fin,
                    hora_fin__gt=hora_inicio,
                    estado='confirmada'
                ).exclude(pk=id)

                if conflictos_cancha.exists():
                    return JsonResponse({'error': 'La cancha ya tiene una reserva confirmada en este horario.'}, status=400)
                
                
                if equipamientos_nombres:
                # Buscar los equipamientos por nombre y verificar disponibilidad
                    equipamientos = Inventario.objects.filter(nombre__in=equipamientos_nombres)
                    conflictos_equipamiento = ReservaEquipamiento.objects.filter(
                        equipamiento__in=equipamientos,
                        reserva__fecha=fecha,
                        reserva__hora_inicio__lt=hora_fin,
                        reserva__hora_fin__gt=hora_inicio,
                        reserva__estado='confirmada'
                    ).exclude(reserva=reserva)

                    if conflictos_equipamiento.exists():
                        return JsonResponse({'error': 'Uno o más equipamientos ya están reservados en este horario.'}, status=400)

            # Actualizar los datos de la reserva
            reserva.cancha = cancha
            reserva.fecha = fecha
            reserva.hora_inicio = hora_inicio
            reserva.hora_fin = hora_fin
            reserva.estado = estado
            reserva.save()

            # Actualizar los equipamientos asociados
            if equipamientos_nombres:
                reserva.equipamiento_reservado.clear()  # Elimina todos los equipamientos actuales
                for equipamiento in equipamientos:
                    ReservaEquipamiento.objects.create(reserva=reserva, equipamiento=equipamiento)

            return JsonResponse({'message': 'Reserva editada correctamente.'}, status=200)
        
        except Reserva.DoesNotExist:
            return JsonResponse({'error': 'Reserva no encontrada.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al decodificar el JSON.'}, status=400)
        except Exception as e:
            print(f'Error al editar la reserva: {e}')
            return JsonResponse({'error': 'Error al editar la reserva.'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido. Usa PUT.'}, status=405)
   
@csrf_exempt
def crear_reserva(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usuario_id = data.get('usuario')
            cancha_id = data.get('cancha')
            subcancha_id = data.get('subcanchas')
            fecha = data.get('fecha')
            hora_inicio = data.get('horaInicio')
            hora_fin = data.get('horaFin')
            equipamientos_ids = data.get('equipamientos', [])  # Lista de IDs de equipamientos

            print(f'Data: {data}')

            cancha = get_object_or_404(Cancha, pk=cancha_id)
            usuario = get_object_or_404(Usuario, pk=usuario_id)

            # Verificar si subcancha está vacía y asignar None en ese caso
            subcancha = get_object_or_404(Subcancha, pk=subcancha_id) if subcancha_id else None

            # Verificar disponibilidad de la cancha y subcancha en el horario seleccionado
            reservas_cancha = Reserva.objects.filter(
                cancha=cancha,
                fecha=fecha,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            ).exclude(estado='confirmada')

            if reservas_cancha.exists():
                print(f"Ya existen reservas en este horario para la cancha {cancha}: {reservas_cancha}")
                return JsonResponse({'error': 'Ya existe una reserva confirmada en este horario para esta cancha'}, status=400)

            if subcancha:
                reservas_subcancha = Reserva.objects.filter(
                    subcancha=subcancha,
                    fecha=fecha,
                    hora_inicio__lt=hora_fin,
                    hora_fin__gt=hora_inicio,
                ).exclude(estado='confirmada')
                if reservas_subcancha.exists():
                    return JsonResponse({'error': 'La subcancha está ocupada en ese horario'}, status=400)
                
            # Crear la nueva reserva
            reserva = Reserva.objects.create(
                cancha=cancha,
                subcancha=subcancha,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                estado='pendiente',
                usuario=usuario
            )
            print(f'Reserva creada: {reserva}')

            # Asociar los equipamientos seleccionados a la reserva
            for equipamiento_id in equipamientos_ids:
                equipamiento = get_object_or_404(Inventario, pk=equipamiento_id)
                ReservaEquipamiento.objects.create(
                    reserva=reserva,
                    equipamiento=equipamiento
                )

            return JsonResponse({'message': 'Reserva creada exitosamente'}, status=200)

        except Exception as e:
            print(f'Error al crear reserva: {e}')
            traceback.print_exc()
            return JsonResponse({'error': 'Error desconocido'}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)

def subcanchas_disponibles(request):
    # print("Solicitud recibida para obtener subcanchas disponibles.")  # Indica que se ha recibido una solicitud
    try:
        cancha_id = request.GET.get('cancha')
        # print(f'Id recibido: {cancha_id}')
        # Obtener la cancha por su ID
        cancha = Cancha.objects.get(pk=cancha_id)
        # print(f"Cancha obtenida: {cancha.nombre} con capacidad de subcanchas: {cancha.capacidad_subcanchas}")  # Imprime detalles de la cancha

        # Obtener las subcanchas que ya están creadas para esta cancha
        subcanchas_creadas = list(Subcancha.objects.filter(cancha=cancha).values('id', 'nombre'))
        # print(f"Subcanchas creadas encontradas: {subcanchas_creadas}")  # Muestra las subcanchas encontradas

        return JsonResponse(subcanchas_creadas, safe=False, status=200)  # Devolver los datos como JSON
    except Exception as e:
        print(f"Error al listar subcanchas disponibles: {e}")  # Imprimir el error en el servidor
        return JsonResponse({'error': 'Error al listar subcanchas disponibles'}, status=500)  # Internal Server Error
    
def listar_horas_cancha(request):
    # print(f'Solicitud recibida para obtener horas ocupadas por cancha.')
    try:
        cancha_id = request.GET.get('cancha')
        reservas = Reserva.objects.filter(cancha=cancha_id)
        
        lista_reservas = []

        for reserva in reservas:
            lista_reservas.append({
                'id': reserva.id,
                'usuario': reserva.usuario.username,  # Puedes acceder a otros campos de usuario si es necesario
                'cancha': reserva.cancha.nombre if reserva.cancha else None,
                'subcancha': reserva.subcancha.nombre if reserva.subcancha else None,
                'fecha': reserva.fecha,
                'hora_inicio': reserva.hora_inicio,
                'hora_fin': reserva.hora_fin,
                'estado': reserva.estado,
                'equipamiento_reservado': [equipamiento.nombre for equipamiento in reserva.equipamiento_reservado.all()]
            })
            
        return JsonResponse(lista_reservas, safe=False, status=200)
        
    except Exception as e:
        print(f'Error al listar horas ocupadas: {e}')
        return JsonResponse({'error': 'Error al listar horas ocupadas'}, status=500)
    
#############################
#######EQUIPAMIENTO##########
#############################    
@csrf_exempt
def crear_equipamiento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            cantidad = data.get('cantidad')
            cantidad_total = data.get('cantidad_total')
            descripcion = data.get('descripcion')

            print(f'Data: {data}')

            equipamiento = Inventario.objects.create(
                nombre=nombre,
                cantidad_disponible=cantidad,
                cantidad_total=cantidad_total,
                descripcion=descripcion
            )
            # print(f'Equipamiento creado: {equipamiento}')

            return JsonResponse({'message': 'Equipamiento creado exitosamente'}, status=200)

        except Exception as e:
            print(f'Error al crear equipamiento: {e}')
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)

def listar_equipamiento(request):
    try:
        equipamiento = Inventario.objects.all().values('id', 'nombre', 'cantidad_total', 'cantidad_disponible', 'descripcion')  # Obtener solo los campos necesarios
        equipamiento_list = list(equipamiento)  # Convertir a lista
        print(equipamiento_list)
        return JsonResponse(equipamiento_list, safe=False, status=200)  # Devolver los datos como JSON
    except Exception as e:
        print(f"Error al listar equipamiento: {e}")  # Imprimir el error en el servidor
        return JsonResponse({'error': 'Error al listar equipamiento'}, status=500)
    
@csrf_exempt
def editar_equipamiento(request):
    if request.method == 'PUT':
        id = request.GET.get('id')
        try:
            body_unicode = request.body.decode('utf-8')  # Decodificar el cuerpo de la solicitud
            body_data = json.loads(body_unicode)  # Cargar el cuerpo como JSON
            nombre = body_data.get('nombre')
            cantidad = body_data.get('cantidad')
            cantidad_total = body_data.get('cantidad_total')
            descripcion = body_data.get('descripcion')
            
            print(f'Body data: {body_data}')

            equipamiento = Inventario.objects.get(pk=id)  # Obtener el equipamiento por ID

            # Actualizar los campos del equipamiento
            equipamiento.nombre = nombre
            equipamiento.cantidad_disponible = cantidad
            equipamiento.cantidad_total = cantidad_total
            equipamiento.descripcion = descripcion
            equipamiento.save()  # Guardar los cambios en la base de datos

            return JsonResponse({'message': 'Equipamiento editado correctamente.'}, status=200)  # OK
        except Inventario.DoesNotExist:
            return JsonResponse({'error': 'Equipamiento no encontrado.'}, status=404)
        
@csrf_exempt
def eliminar_equipamiento(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        try:
            equipamiento = Inventario.objects.get(pk=id)
            equipamiento.delete()
            return JsonResponse({'message': 'Equipamiento eliminado correctamente.'}, status=204)  # No Content
        except Inventario.DoesNotExist:
            return JsonResponse({'error': 'Equipamiento no encontrado.'}, status=404)
        
        except Exception as e:
            print(f'Error al eliminar el equipamiento: {e}')
            return JsonResponse({'error': 'Error al eliminar el equipamiento.'}, status=500)
        
    else:
        return JsonResponse({'error': 'Método no permitido. Usa DELETE.'}, status=405)
    
def equipamiento_disponible(request):
    print("Solicitud recibida para obtener equipamiento disponible.")
    try:
        if request.method == 'GET':
            fecha = request.GET.get('fecha')
            hora_inicio = request.GET.get('horaInicio')
            hora_fin = request.GET.get('horaFin')
            
            equipamiento = Inventario.objects.filter(cantidad_disponible__gt=0).values('id', 'nombre', 'cantidad_disponible')
            equipamiento_list = list(equipamiento)
            print(equipamiento_list)
            return JsonResponse(equipamiento_list, safe=False, status=200)
    except:
        return JsonResponse({'error': 'Error al listar equipamiento disponible'}, status=500)
            
#############################
#######EQUIPAMIENTO##########
#############################    