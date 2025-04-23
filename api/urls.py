from django.urls import path, include
from .views import *
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'notifications', NotificationView)
router.register(r'reservaciones', reservacionesViewSet, basename='reservaciones')
router.register(r'hoteles', hotelesViewSet, basename='hoteles')
router.register(r'notifications', NotificationViewSet)
router.register(r'usuarios', cuentasViewSet)

urlpatterns = [
    # path('notifications/', NotificationView.as_view(), name='notifications'),
    # path('notifications/', NotificationView.as_view({'post': 'post'}), name='notifications'),
    path('', include(router.urls)), 
    path('obtener-tipo-usuario/', ApigetUserType.as_view()),

    # path('reservaciones/', reservacionesViewSet.as_view(), name='reservaciones'),
]