from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .datos import LIBROS, buscar_libro


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
    if genero:
        libros = [libro for libro in LIBROS if libro["genero"] == genero]
    else:
        libros = LIBROS
    return render(
        request,
        "app_catalogo/lista.html",
        {"libros": libros, "genero": genero},
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
    total = len(LIBROS)
    disponibles = sum(1 for libro in LIBROS if libro["disponible"])
    prestados = total - disponibles
    porcentaje_disponible = round(disponibles * 100 / total) if total else 0

    cantidad_por_genero = {}
    for libro in LIBROS:
        genero = libro["genero"]
        cantidad_por_genero[genero] = cantidad_por_genero.get(genero, 0) + 1
    libros_por_genero = [
        {"genero": genero, "cantidad": cantidad}
        for genero, cantidad in sorted(cantidad_por_genero.items())
    ]

    contexto = {
        "total": total,
        "disponibles": disponibles,
        "prestados": prestados,
        "porcentaje_disponible": porcentaje_disponible,
        "libros_por_genero": libros_por_genero,
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
    libro = buscar_libro(libro_id)
    if libro is None:
        raise Http404("El libro no existe")
    return render(request, "app_catalogo/detalle.html", {"libro": libro})


def hola(request):
    return HttpResponse("Hola desde Django")


def cuadrado(request, numero):
    resultado = numero ** 2
    return HttpResponse(f"El cuadrado de {numero} es {resultado}")


class ContactoView(TemplateView):
    template_name = "app_catalogo/contacto.html"


class AcercaView(TemplateView):
    template_name = "app_catalogo/acerca.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["version"] = "1.0"
        return contexto
