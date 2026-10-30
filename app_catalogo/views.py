from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from .datos import LIBROS
from .models import libro


def inicio(request):
    libros_disponibles = sum(1 for libro in LIBROS if libro["disponible"])
    libros_prestados = len(LIBROS) - libros_disponibles
    contexto = {
        "nombre_sitio": "Catálogo de libros",
        "total": len(LIBROS),
        "libros_disponibles": libros_disponibles,
        "libros_prestados": libros_prestados,
    }
    return render(request, "app_catalogo/inicio.html", contexto)


def lista_libros(request):
    genero = request.GET.get("genero", "")
    libros = libro.objects.order_by("id")
    if genero:
        libros = libros.filter(genero=genero)
    return render(
        request,
        "app_catalogo/lista.html",
        {"libros": libros, "genero": genero},
    )


def buscar_libros_por_nombre(request, nombre=""):
    nombre = nombre or request.GET.get("nombre", "").strip()
    libros = libro.objects.none()
    if nombre:
        libros = libro.objects.filter(titulo__icontains=nombre).select_related(
            "editorial",
            "tema",
        ).order_by("id")
    return render(
        request,
        "app_catalogo/buscar_libros.html",
        {"libros": libros, "nombre": nombre},
    )


def autores(request):
    cantidad_por_autor = {}
    for libro in LIBROS:
        autor = libro["autor"]
        cantidad_por_autor[autor] = cantidad_por_autor.get(autor, 0) + 1
    lista_autores = [
        {"nombre": nombre, "cantidad_libros": cantidad}
        for nombre, cantidad in sorted(cantidad_por_autor.items())
    ]
    return render(
        request,
        "app_catalogo/autores.html",
        {"autores": lista_autores},
    )


def logica(request):
    disponibles = sum(1 for libro in LIBROS if libro["disponible"])
    libros_mostrar = [libro for libro in LIBROS if libro["disponible"]]
    contexto = {
        "disponibles": disponibles,
        "libros": libros_mostrar,
    }
    return render(request, "app_catalogo/logica.html", contexto)


def sugerir(request):
    contexto = {}
    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        if titulo:
            contexto["titulo_sugerido"] = titulo
        else:
            contexto["error"] = "Escribe un título"
    return render(request, "app_catalogo/sugerir.html", contexto)


def detalle_libro(request, libro_id):
    libro_obj = get_object_or_404(libro, pk=libro_id)
    return render(request, "app_catalogo/detalle.html", {"libro": libro_obj})


def hola(request):
    return HttpResponse("Hola desde Django")


def cuadrado(request, numero):
    resultado = numero ** 2
    return HttpResponse(f"El cuadrado de {numero} es {resultado}")


def contacto(request):
    contexto = {}
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        motivo = request.POST.get("motivo", "").strip()
        mensaje = request.POST.get("mensaje", "").strip()
        acepta_terminos = request.POST.get("acepta_terminos")

        if nombre and correo and motivo and mensaje and acepta_terminos:
            contexto["enviado"] = True
            contexto["nombre"] = nombre
        else:
            contexto["error"] = "Completa todos los campos obligatorios."
            contexto.update(
                {
                    "nombre": nombre,
                    "correo": correo,
                    "motivo": motivo,
                    "mensaje": mensaje,
                }
            )
    return render(request, "app_catalogo/contacto.html", contexto)


class AcercaView(TemplateView):
    template_name = "app_catalogo/acerca.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["version"] = "1.0"
        return contexto
