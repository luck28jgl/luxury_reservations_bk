from rest_framework import serializers
from .models import *

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ReservacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = reservaciones
        fields = '__all__'

class AcoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = usuario
        fields = '__all__'