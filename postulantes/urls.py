from django.urls import path
#from .views import registro_postulante
from . import views

app_name = 'postulantes'

urlpatterns = [
    path('registrar/', views.registro_postulante, name='registrar_postulante'),
    path('exito/', views.registro_exitoso, name='registro_exitoso'),
    path('listar/', views.listar_postulantes, name='listar_postulantes'),
    path('generar_pdf/<int:pk>', views.postulante_print, name='generar_pdf' ),
    path('cuota/', views.storage_quota, name='storage_quota')
]