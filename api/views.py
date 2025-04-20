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
from django.contrib.auth import authenticate
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
		# makeLogs(request,'actualización de usuarios', 'ha registrado un nuevo Staff')
		return Response({'status':True, 'message':'Reservación registrada correctamente.'})


class cuentasViewSet(viewsets.ModelViewSet):
	queryset = usuario.objects.all().exclude(tipo=0)
	serializer_class = AcoutSerializer

