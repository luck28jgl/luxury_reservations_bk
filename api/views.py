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
			# if not usru.tipo in [0]:
			# 	return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
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
		return Response({'status':True, 'tipo': user.usuario.tipo, 'id': user.usuario.id})
		
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
	queryset = reservaciones.objects.all()
	serializer_class = ReservacionesSerializer
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
		enf = reservaciones.objects.create(
			email=data['email'],
			uduario=data['uduario'],
			hotel=str(data['hotel']),
			plan=str(data['plan']),
			tip_hab=str(data['tip_hab']),
			tip_vista=str(data['tip_vista']),
		)
		enf.save()
		# Render the email template with the reservation data
		email_content = render_to_string(
			'email-notificaciones.html',  # Path to your template
			{
				'mensaje': f"Se ha creado una nueva reservación con los siguientes datos:\n"
						f"Email: {data['email']}\n"
						f"Usuario: {data['uduario']}\n"
						f"Hotel: {data['hotel']}\n"
						f"Plan: {data['plan']}\n"
						f"Tipo de Habitación: {data['tip_hab']}\n"
						f"Tipo de Vista: {data['tip_vista']}"
			}
		)

		# Send the email
		email = EmailMessage(
			subject="Nueva Reservación Creada",
			body=email_content,
			from_email=settings.DEFAULT_FROM_EMAIL,  # Usar el valor configurado en settings.py
			# from_email="noreply@tu-dominio.com",  # Replace with your sender email
			# to=["connyi.moreno@gmail.com","fredyescobar623@gmail.com"],  # Replace with the fixed recipient email
			to=["andrea2030ibarra@gmail.com"],  # Replace with the fixed recipient email
		)
		email.content_subtype = "html"  # Specify that the email content is HTML
		email.send()

		return Response({'status': True, 'message': 'Reservación registrada correctamente.'})


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
	

