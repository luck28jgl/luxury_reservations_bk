from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import *
# from .serializers import *
# from rest_framework.decorators import action

# from .utils.ArchivosFunciones import generate_rsa_key_pair, generar_hash, desencriptar_hash
# from .utils.amazon import subirArchivosAmazon, eliminarArchivoAmazon
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token
from django.http import HttpRequest, HttpResponse
# from .utils.emails import send_email_notification
from rest_framework.permissions import AllowAny
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.db.models.functions import Concat
from rest_framework.decorators import action
# from django.contrib.auth import authenticate
from rest_framework.response import Response
# from .utils.AppToken import get_access_token
# from .utils.generacionDocumentos import generarDocumento
from django.db.models import F, Sum, Value
from django.core.mail import EmailMessage
from api.customPagination import CustomPagination

# from .utils.Ubicacion import puntoEnZona, puntoEnZonaNorma
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.http import JsonResponse
# from .utils.colonias import COLONIAS
from rest_framework import viewsets
# from dateutil import relativedelta
from rest_framework import status
from django.conf import settings
from datetime import timedelta
from django.db.models import Q
# from .utils.pdf import getPDF
# from .utils.tiposZonas import NORMAS_ZONAS
from .serializers import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from rest_framework.decorators import api_view
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import logout, login
from django.utils import timezone
from django.contrib.auth import authenticate
from datetime import datetime  # Importar el módulo datetime
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.core.files.storage import default_storage

user = authenticate(username='tes66@gmail.com', password='123456')
print(user)  # Debería devolver el objeto del usuario si las credenciales son correctas

# print(settings.TEMPLATES[0]['DIRS']) 
class CustomTokenCreateView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		print(f"Username: {username}, Password: {password}")  # Depuración
		usr = authenticate(username=username, password=password)
		print(f"Authenticated user: {usr}")  # Depuración

		if usr is not None:
			usru = usuario.objects.get(user=usr)
			print(f"User type: {usru.tipo}")  # Depuración
			if not usru.tipo in [0, 1]:
				return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
			token, created = Token.objects.get_or_create(user=usr)
			login(request, user)
			return Response({'auth_token': token.key, 'status': True})
		else:
			return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):

	def post(self, request):
		try:
			logout(request)
			return Response(status=status.HTTP_204_NO_CONTENT)
		except Token.DoesNotExist:
			return Response({'error': 'Token not found'}, status=status.HTTP_400_BAD_REQUEST)

class ApigetUserType(APIView):
	authentication_classes = [SessionAuthentication]
	permission_classes = [AllowAny]

	def post(self, request):
		data=request.data
		print(data)
		user = User.objects.get(username=data['username'])
		return Response({'status':True, 'tipo': user.usuario.tipo, 'id': user.usuario.id, 'nombre': user.first_name})
		
class NotificationViewSet(viewsets.ModelViewSet):
	queryset = Notification.objects.all().order_by('-id')
	serializer_class = NotificationSerializer

	def list(self, request):
		data = request.GET
		tmp = self.get_queryset()
		if data.get('mensaje'):
			tmp = tmp.filter(mensaje__icontains=data['mensaje'])
		queryset = self.filter_queryset(tmp)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)
    
class reservacionesViewSet(viewsets.ModelViewSet):
	queryset = reservaciones.objects.all().order_by('-id')
	serializer_class = ReservacionesSerializer
	authentication_classes = [SessionAuthentication]
	parser_classes = [JSONParser, MultiPartParser, FormParser]

	@action(detail=False, methods=['post'], url_path='compra-aprobada')
	def compra_aprobada(self, request):
		reservacion_id = request.data.get('id')
		# archivo = request.FILES.get('pago')
		reservacion = reservaciones.objects.get(id=reservacion_id)
		if not reservacion:
			return Response({'error': 'Reservación no encontrada.'}, status=404)
		reservacion.pagado = True
		reservacion.save()

		return Response({'message': 'Reservacion completada extitosamente.'})

	@action(detail=False, methods=['post'], url_path='enviar-comprovante')
	def enviar_comprovante(self, request):
		reservacion_id = request.data.get('id')
		archivo = request.FILES.get('archivo')

		if not reservacion_id or not archivo:
			return Response({'error': 'ID y archivo son requeridos.'}, status=400)

		try:
			reservacion = reservaciones.objects.get(id=reservacion_id)
		except reservaciones.DoesNotExist:
			return Response({'error': 'Reservación no encontrada.'}, status=404)

		# Guardar el archivo en S3
		file_path = f'comprobantes/{archivo.name}'
		saved_file = default_storage.save(file_path, archivo)

		# Generar la URL pública del archivo en S3
		file_url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{saved_file}'

		# Guardar la URL completa en el modelo
		reservacion.img_enviada = file_url
		reservacion.clent_envie_img = True
		reservacion.save()

		return Response({'message': 'Archivo subido exitosamente.', 'file_url': file_url})
	
	# 	@action(detail=False, methods=['post'], url_path='enviar-comprovante')
	# def enviar_comprovante(self, request):
	# 	reservacion_id = request.data.get('id')
	# 	archivo = request.FILES.get('archivo')

	# 	if not reservacion_id or not archivo:
	# 		return Response({'error': 'ID y archivo son requeridos.'}, status=400)

	# 	try:
	# 		reservacion = reservaciones.objects.get(id=reservacion_id)
	# 	except reservaciones.DoesNotExist:
	# 		return Response({'error': 'Reservación no encontrada.'}, status=404)

	# 	# Guardar el archivo en S3
	# 	file_path = f'comprobantes/{archivo.name}'
	# 	default_storage.save(file_path, archivo)

	# 	# Guardar el archivo en S3
	# 	file_path = f'comprobantes/{archivo.name}'
	# 	saved_file = default_storage.save(file_path, archivo)

	# 	# Generar la URL pública del archivo en S3
	# 	file_url = f'{settings.MEDIA_URL}{saved_file}'

	# 	# Guardar la URL completa en el modelo
	# 	reservacion.img_enviada = file_url
	# 	reservacion.clent_envie_img = True
	# 	reservacion.save()

	# 	return Response({'message': 'Archivo subido exitosamente.', 'file_url': file_url})

	@action(detail=True, methods=['delete'], url_path='delete-reservation')
	def delete_reservation(self, request, pk=None):
		try:
			# Obtener la reservación por ID
			reservation = self.get_object()
			reservation.delete()
			return Response({'status': True, 'message': 'Reservación eliminada correctamente.'}, status=status.HTTP_200_OK)
		except reservaciones.DoesNotExist:
			return Response({'status': False, 'message': 'Reservación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

	@action(detail=False, methods=['post'], url_path='create-for-user')
	def create_for_user(self, request):
		"""
		Crea una reservación y la asocia a un cliente específico.
		"""
		data = request.data
		usuario_id = data.get('usuario_id')  # ID del cliente al que se ligará la reservación

		# Validar que el cliente exista
		try:
			cliente = usuario.objects.get(id=usuario_id)
		except usuario.DoesNotExist:
			return Response({'status': False, 'message': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
	
		# Crear la reservación
		reservacion = reservaciones.objects.create(
			email=data['email'],
			uduario=data['uduario'],  # Asociar la reservación al cliente
			price=data['price'],
			usuario_relation=cliente,  # Asociar la reservación al cliente
			hotel=data['hotel'],
			plan=data['plan'],
			tip_hab=data['tip_hab'],
			tip_vista=data['tip_vista'],
			cuentas_pesonas=data['cuentas_pesonas'],
			usuario_on=data['usuario_on'],
			pagado=False,## quiero que este campo sea false siempre
			fecha_de_creacion=datetime.now().strftime('%d/%m/%Y'),
			desde=data['desde'],
			hasta=data['hasta'],
		)
		reservacion.save()

		# Render the email template with the reservation data
		email_content = render_to_string(
			'email-notificaciones-public.html',  # Path to your template
			{
				'email': data['email'],
				'uduario': data['uduario'],
				'price': data['price'],
				'usuario_con_cuenta_iniciada': cliente.user.first_name,
				'hotel': data['hotel'],
				'plan': data['plan'],
				'tip_hab': data['tip_hab'],
				'tip_vista': data['tip_vista'],
				'desde': data['desde'],
				'hasta': data['hasta'],
				'cuentas_pesonas': data['cuentas_pesonas'],
				'fecha_de_creacion': datetime.now().strftime('%d/%m/%Y'),
			}
		)

		# Send the first email
		email = EmailMessage(
			subject="Nueva Reservación Creada",
			body=email_content,
			from_email=settings.DEFAULT_FROM_EMAIL,  # Usar el valor configurado en settings.py
			# to=["connyi.moreno@gmail.com", "fredyescobar623@gmail.com"],  # Replace with the fixed recipient email
			to=["Luckibarra15@gmail.com"],  # Replace with the fixed recipient email
		)
		email.content_subtype = "html"  # Specify that the email content is HTML
		email.send()

		# Render the third email template with the hotel and download button
		third_email_content = render_to_string(
			'email-clientes.html',  # Path to your client-specific template
			{
				'uduario': data['uduario'],
				'email': data['email'],
				'hotel': data['hotel'],
				'pdf_url': "https://mi-api-imagenes.s3.us-east-2.amazonaws.com/media/Ficha_de_pago_con_inicio_de_sesion.pdf",  # quiero que la url que mande aqui sea esta " https://mi-api-imagenes.s3.us-east-2.amazonaws.com/media/Ficha_de_pago_con_inicio_de_sesion.pdf "

			}
		)

		# Send the third email
		third_email = EmailMessage(
			subject="Ficha de pago de su Reservación",
			body=third_email_content,
			from_email=settings.DEFAULT_FROM_EMAIL,  # Usar el valor configurado en settings.py
			to=["Luckibarra15@gmail.com", data['email']],  # Send to the client's email
			# to=[data['email']],  # Send to the client's email
		)
		third_email.content_subtype = "html"  # Specify that the email content is HTML
		third_email.send()

		return Response({'status': True, 'message': 'Reservación registrada correctamente.'})

	@action(detail=False, methods=['get'], url_path='user-reservations')
	def user_reservations(self, request):
		"""
		Lista todas las reservaciones asociadas a un cliente específico.
		"""
		usuario_id = request.query_params.get('usuario_id')  # Obtener el ID del cliente desde los parámetros de consulta

		# Validar que el cliente exista
		try:
			cliente = usuario.objects.get(id=usuario_id)
		except usuario.DoesNotExist:
			return Response({'status': False, 'message': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

		# Obtener las reservaciones asociadas al cliente
		reservations = cliente.reservaciones.all().order_by('-id')  # Usar el related_name definido en el modelo y ordenar por ID
		serializer = self.get_serializer(reservations, many=True)

		return Response({'status': True, 'reservations': serializer.data})

	def list(self, request):
		data = request.GET
		tmp = self.get_queryset().filter(usuario_on=True)##filtrar por el campo usuario_on en True
		if data.get('filt'):
			tmp = tmp.filter(mensaje__icontains=data['filt'])
		queryset = self.filter_queryset(tmp)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	##crea una api de enlistado igual a la de lista pero que filtre por el campo usuario_on en False
	@action(detail=False, methods=['get'], url_path='priv')
	def list_reservations(self, request):
		data = request.GET
		tmp = self.get_queryset().filter(usuario_on=False)
		if data.get('filt'):
			tmp = tmp.filter(mensaje__icontains=data['filt'])
		queryset = self.filter_queryset(tmp)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request):
		data = request.data
		enf = reservaciones.objects.create(
			email=data['email'],
			uduario=data['uduario'],
			price=data['price'],
			hotel=str(data['hotel']),
			cuentas_pesonas=str(data['cuentas_pesonas']),
			usuario_on=str(data['usuario_on']),
			pagado=False,
			fecha_de_creacion=datetime.now().strftime('%d/%m/%Y'),
			desde=str(data['desde']),
			hasta=str(data['hasta']),
			plan=str(data['plan']),
			tip_hab=str(data['tip_hab']),
			tip_vista=str(data['tip_vista']),
		)
		enf.save()
		# Render the email template with the reservation data
		email_content = render_to_string(
			'email-notificaciones.html',  # Path to your template
			{
				'email': data['email'],
				'uduario': data['uduario'],
				'hotel': data['hotel'],
				'price': data['price'],
				'plan': data['plan'],
				'tip_hab': data['tip_hab'],
				'tip_vista': data['tip_vista'],
				'desde': data['desde'],
				'hasta': data['hasta'],
				'cuentas_pesonas': data['cuentas_pesonas'],
				'fecha_de_creacion': datetime.now().strftime('%d/%m/%Y'),
			}
		)

		# Send the email
		email = EmailMessage(
			subject="Nueva Reservación Creada",
			body=email_content,
			from_email=settings.DEFAULT_FROM_EMAIL,  # Usar el valor configurado en settings.py
			# from_email="noreply@tu-dominio.com",  # Replace with your sender email
			# to=["connyi.moreno@gmail.com","fredyescobar623@gmail.com"],  # Replace with the fixed recipient email
			to=["Luckibarra15@gmail.com"],# Replace with the fixed recipient email
		)
		email.content_subtype = "html"  # Specify that the email content is HTML
		email.send()
		
		# Render the third email template with the hotel and download button
		third_email_content = render_to_string(
			'email-clientes.html',  # Path to your client-specific template
			{
				'uduario': data['uduario'],
				'hotel': data['hotel'],
				'price': data['price'],
				'email': data['email'],
				'pdf_url': "https://mi-api-imagenes.s3.us-east-2.amazonaws.com/media/Ficha_de_pago_fuera_de_luxe.pdf",  # URL to the fixed PDF file
			}
		)

		# Send the third email
		third_email = EmailMessage(
			subject="Ficha de pago de su Reservación",
			body=third_email_content,
			from_email=settings.DEFAULT_FROM_EMAIL,  # Usar el valor configurado en settings.py
			to=["Luckibarra15@gmail.com", data['email']],  # Send to the client's email
			# to=[data['email']],  # Send to the client's email
		)
		third_email.content_subtype = "html"  # Specify that the email content is HTML
		third_email.send()

		return Response({'status': True, 'message': 'Reservación registrada correctamente.'})

class hotelesViewSet(viewsets.ModelViewSet):
	queryset = hoteles.objects.all().order_by('-id')
	serializer_class = HotelesSerializer
	authentication_classes = [SessionAuthentication]

	@action(detail=True, methods=['delete'], url_path='delete-reservation')
	def delete_reservation(self, request, pk=None):
		try:
			# Obtener la reservación por ID
			reservation = self.get_object()
			reservation.delete()
			return Response({'status': True, 'message': 'Reservación eliminada correctamente.'}, status=status.HTTP_200_OK)
		except reservaciones.DoesNotExist:
			return Response({'status': False, 'message': 'Reservación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

	def list(self, request):
		data = request.GET
		tmp = self.get_queryset()
		if data.get('filt'):
			tmp = tmp.filter(mensaje__icontains=data['filt'])
		queryset = self.filter_queryset(tmp)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request):
		data = request.data
		archivo = request.FILES.get('archivo')  # Obtener el archivo enviado

		if archivo:
			# Crear la carpeta media/hoteles si no existe
			media_path = os.path.join(settings.MEDIA_ROOT, 'hoteles')
			if not os.path.exists(media_path):
				os.makedirs(media_path)

			# Guardar el archivo en la carpeta media/hoteles
			file_path = os.path.join('hoteles', archivo.name)
			full_path = os.path.join(settings.MEDIA_ROOT, file_path)
			default_storage.save(full_path, ContentFile(archivo.read()))

			# Obtener la URL completa del archivo
			img_url = f"{settings.MEDIA_URL}{file_path}".replace('\\', '/')

			# Crear el objeto del modelo hoteles
			enf = hoteles.objects.create(
				Nombre=data['nombre'],
				price=data['price'],
				img=img_url,  # Guardar la URL en el campo img
			)
			enf.save()

			return Response({'status': True, 'message': 'Hotel registrado correctamente.', 'img_url': img_url})
		else:
			return Response({'status': False, 'message': 'No se proporcionó un archivo.'}, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, *args, **kwargs):
		data = request.data

		hotel = get_object_or_404(hoteles, pk=data['id'])
		hotel.Nombre = data.get('nombre', hotel.Nombre )
		hotel.price = data.get('price', hotel.price)
		hotel.save()

		return Response({
			'id': hotel.id,
			'status': True,
			'message': 'Hotel actualizado correctamente'
		})


class cuentasViewSet(viewsets.ModelViewSet):
	queryset = usuario.objects.all().exclude(tipo=0)
	serializer_class = AcoutSerializer
	authentication_classes = [SessionAuthentication]

	def create(self, request):
		data = request.data
		enf = User.objects.create(
			first_name=data['first_name'],
			last_name=data['first_name'],
			email=data['email'],
			username=data['email'],
			is_staff=False,
			is_superuser=True
		)
		enf.set_password(data['password'])
		enf.save()
		tipo_usuario = data.get('tipo_usuario')

		us = usuario.objects.create(user=enf, tipo=tipo_usuario)
		us.save()
		# makeLogs(request,'actualización de usuarios', 'ha registrado un nuevo Staff')
		return Response({'status':True, 'message':'Staff registrado correctamente.'})
	

