# from django.db import models
from django.db import models, migrations
from django.contrib.postgres.operations import HStoreExtension, UnaccentExtension
from django.contrib.postgres.fields import HStoreField
from django.contrib.auth.models import User

class Notification(models.Model):
    mensaje = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.

class hoteles(models.Model):
    Nombre = models.TextField(default='') #
    price = models.TextField(default='') #
    img = models.TextField(default='') #
    impuesto_por_hotel = models.IntegerField(default=0)
    iva = models.IntegerField(default=16)
    precio_adult = models.IntegerField(default=0)
    precio_nino = models.IntegerField(default=0)
    lista_ejemplo = models.JSONField(default=list, blank=True, null=True)

class reservaciones(models.Model):
    email = models.TextField(default='', null=True, blank=True) # Habitantes por hectárea
    uduario = models.TextField(default='', null=True, blank=True) # Cuartos por hectárea
    usuario_relation = models.ForeignKey('usuario', on_delete=models.CASCADE, related_name='reservaciones', null=True, blank=True)
    hotel = models.TextField(default='', null=True, blank=True) # Viviendas por hectareas
    plan = models.TextField(default='', null=True, blank=True) # superficie minima del terreno
    tip_hab = models.TextField(default='', null=True, blank=True) # superficie minima del terreno
    tip_vista = models.TextField(default='', null=True, blank=True) # superficie minima del terreno
    cuentas_pesonas = models.TextField(default='', null=True, blank=True) # superficie minima del terreno
    usuario_on = models.BooleanField(default=False) # superficie minima del terreno
    pagado = models.BooleanField(default=False, null=True, blank=True) # superficie minima del terreno
    fecha_de_creacion = models.DateTimeField(auto_now=True)
    desde = models.TextField(default='', null=True, blank=True)  # Cambiado a TextField
    hasta = models.TextField(default='', null=True, blank=True)  # Cambiado a TextField
    price = models.TextField(default='', null=True, blank=True)  # Cambiado a TextField
    clent_envie_img = models.BooleanField(default=False, null=True, blank=True)
    img_enviada = models.TextField(default='', null=True, blank=True)

class usuario(models.Model):

    class Status(models.IntegerChoices):
        admin = 0
        cliente = 1

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.IntegerField(choices=Status.choices, default=1)
    emails_admin = models.ForeignKey(Notification, on_delete=models.CASCADE, null=True)
    # reservacion = models.ForeignKey(reservaciones, on_delete=models.CASCADE, null=True)

