from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/nombre/', views.buscar_libros_por_nombre, name='buscar_libros_por_nombre'),
    path('libros/nombre/<str:nombre>/', views.buscar_libros_por_nombre, name='buscar_libros_por_nombre'),
    path('libros/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('autores/', views.autores, name='autores'),
    path('autores/buscar/', views.buscar_autor, name='buscar_autor'),
    path('autores/buscar/<str:criterio>/', views.buscar_autor, name='buscar_autor'),
    path('logica/', views.logica, name='logica'),
    path('sugerir/', views.sugerir, name='sugerir'),
    path('personas/registrar/', views.registrar_persona, name='registrar_persona'),
    path('usuarios/registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/completar/<int:usuario_id>/', views.completar_registro, name='completar_registro'),
    path('usuarios/consultar/', views.consultar_usuario, name='consultar_usuario'),
    path('usuarios/consultar/<str:usuario_id>/', views.consultar_usuario, name='consultar_usuario'),
    path('acerca/', views.AcercaView.as_view(), name='acerca'),
    path('hola/', views.hola, name='hola'),
    path('cuadrado/<int:numero>/', views.cuadrado, name='cuadrado'),
]
