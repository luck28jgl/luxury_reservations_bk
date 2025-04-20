from django.urls import path, include
from .views import *
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'notifications', NotificationView)
router.register(r'reservaciones', reservacionesViewSet, basename='reservaciones')
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    # path('notifications/', NotificationView.as_view(), name='notifications'),
    # path('notifications/', NotificationView.as_view({'post': 'post'}), name='notifications'),
    path('', include(router.urls)), 
    # path('reservaciones/', reservacionesViewSet.as_view(), name='reservaciones'),
]