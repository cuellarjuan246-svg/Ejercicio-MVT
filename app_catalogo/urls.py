from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('autores/', views.autores, name='autores'),
    path('logica/', views.logica, name='logica'),
    path('sugerir/', views.sugerir, name='sugerir'),
    path('acerca/', views.AcercaView.as_view(), name='acerca'),
    path('hola/', views.hola, name='hola'),
    path('cuadrado/<int:numero>/', views.cuadrado, name='cuadrado'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
]
