from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from .datos import LIBROS
from .models import autor, estudiante, libro, usuario


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


def registrar_persona(request):
    contexto = {}
    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre", "").strip(),
            "tipo_documento": request.POST.get("tipo_documento", "").strip(),
            "numero_documento": request.POST.get("numero_documento", "").strip(),
            "telefono": request.POST.get("telefono", "").strip(),
            "correo": request.POST.get("correo", "").strip(),
            "fecha_nacimiento": request.POST.get("fecha_nacimiento", "").strip(),
            "genero": request.POST.get("genero", "").strip(),
            "rol": request.POST.get("rol", "").strip(),
        }

        if all(datos.values()):
            if usuario.objects.filter(correo=datos["correo"]).exists():
                contexto["error"] = "Ya existe una persona registrada con ese correo."
            else:
                usuario.objects.create(**datos)
                contexto["registrado"] = True
                contexto["nombre"] = datos["nombre"]
                datos = {}
        else:
            contexto["error"] = "Completa todos los campos obligatorios."

        contexto.update(datos)

    return render(request, "app_catalogo/registrar_persona.html", contexto)


def registrar_usuario(request):
    contexto = {}
    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre", "").strip(),
            "correo": request.POST.get("correo", "").strip(),
            "fecha_nacimiento": request.POST.get("fecha_nacimiento", "").strip(),
            "genero": request.POST.get("genero", "").strip(),
            "rol": request.POST.get("rol", "").strip(),
        }
        roles_validos = dict(usuario._meta.get_field("rol").choices)

        if not all(datos.values()):
            contexto["error"] = "Completa todos los campos obligatorios."
            contexto.update(datos)
        elif datos["rol"] not in roles_validos:
            contexto["error"] = "El rol seleccionado no es válido."
            contexto.update(datos)
        elif usuario.objects.filter(correo=datos["correo"]).exists():
            contexto["error"] = "Ya existe un usuario registrado con ese correo."
            contexto.update(datos)
        else:
            usuario_nuevo = usuario.objects.create(**datos)
            if usuario_nuevo.rol == "estudiante":
                return redirect("completar_registro", usuario_id=usuario_nuevo.id)
            contexto["registrado"] = True
            contexto["nombre"] = usuario_nuevo.nombre

    return render(request, "app_catalogo/registrar_usuario.html", contexto)


def completar_registro(request, usuario_id):
    usuario_obj = get_object_or_404(usuario, pk=usuario_id, rol="estudiante")
    contexto = {"usuario_obj": usuario_obj}

    if estudiante.objects.filter(id=usuario_obj).exists():
        contexto["ya_completo"] = True
        return render(request, "app_catalogo/completar_registro.html", contexto)

    if request.method == "POST":
        datos = {
            "direccion": request.POST.get("direccion", "").strip(),
            "telefono": request.POST.get("telefono", "").strip(),
            "grado_escolar": request.POST.get("grado_escolar", "").strip(),
        }
        if all(datos.values()):
            estudiante.objects.create(id=usuario_obj, **datos)
            contexto["completado"] = True
        else:
            contexto["error"] = "Completa todos los campos obligatorios."
            contexto.update(datos)

    return render(request, "app_catalogo/completar_registro.html", contexto)


def consultar_usuario(request, usuario_id=""):
    usuario_id = usuario_id or request.GET.get("id", "").strip()
    usuario_obj = None
    perfil_estudiante = None
    error = None

    if usuario_id:
        if usuario_id.isdigit():
            usuario_obj = usuario.objects.filter(pk=int(usuario_id)).first()
            if usuario_obj is None:
                error = "No existe ningún usuario con ese ID."
            elif usuario_obj.rol == "estudiante":
                perfil_estudiante = estudiante.objects.filter(id=usuario_obj).first()
        else:
            error = "El ID debe ser un número."

    return render(
        request,
        "app_catalogo/consultar_usuario.html",
        {
            "usuario_id": usuario_id,
            "usuario_obj": usuario_obj,
            "perfil_estudiante": perfil_estudiante,
            "error": error,
        },
    )


def buscar_autor(request, criterio=""):
    criterio = criterio or request.GET.get("autor", "").strip()
    autores_encontrados = autor.objects.none()
    if criterio:
        if criterio.isdigit():
            autores_encontrados = autor.objects.filter(id=int(criterio))
        else:
            autores_encontrados = autor.objects.filter(nombre__icontains=criterio)

    resultados = [
        {
            "autor": autor_obj,
            "libros": libro.objects.filter(autor=autor_obj.nombre).order_by("id"),
        }
        for autor_obj in autores_encontrados
    ]
    return render(
        request,
        "app_catalogo/buscar_autor.html",
        {"resultados": resultados, "criterio": criterio},
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


class AcercaView(TemplateView):
    template_name = "app_catalogo/acerca.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["version"] = "1.0"
        return contexto
