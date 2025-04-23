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

class reservaciones(models.Model):
    email = models.TextField(default='') # Habitantes por hectárea
    uduario = models.TextField(default='') # Cuartos por hectárea
    usuario_relation = models.ForeignKey('usuario', on_delete=models.CASCADE, related_name='reservaciones', null=True, blank=True)
    hotel = models.TextField(default='') # Viviendas por hectareas
    plan = models.TextField(default='') # superficie minima del terreno
    tip_hab = models.TextField(default='') # superficie minima del terreno
    tip_vista = models.TextField(default='') # superficie minima del terreno
    cuentas_pesonas = models.TextField(default='') # superficie minima del terreno
    usuario_on = models.BooleanField(default=True) # superficie minima del terreno
    fecha_de_creacion = models.DateTimeField(auto_now=True)
    desde = models.DateTimeField(auto_now=True)
    hasta = models.DateTimeField(auto_now=True)

class usuario(models.Model):

    class Status(models.IntegerChoices):
        admin = 0
        cliente = 1

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.IntegerField(choices=Status.choices, default=1)
    emails_admin = models.ForeignKey(Notification, on_delete=models.CASCADE, null=True)
    # reservacion = models.ForeignKey(reservaciones, on_delete=models.CASCADE, null=True)

