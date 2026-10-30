from django.db import migrations


LIBROS_EXISTENTES = {
    7: {
        "titulo": "Minecraft: Guía de construcción",
        "autor": "Mojang Studios",
        "genero": "videojuegos",
        "anio_publicacion": 2023,
        "precio": "24.90",
        "ubicacion": "Estante A",
        "estado": "nuevo",
        "disponible": True,
    },
    8: {
        "titulo": "Cocina para todos",
        "autor": "Sofía Herrera",
        "genero": "cocina",
        "anio_publicacion": 2021,
        "precio": "19.50",
        "ubicacion": "Estante B",
        "estado": "nuevo",
        "disponible": True,
    },
    9: {
        "titulo": "Breve historia del mundo",
        "autor": "Ernesto Salas",
        "genero": "historia",
        "anio_publicacion": 2018,
        "precio": "22.00",
        "ubicacion": "Estante C",
        "estado": "usado",
        "disponible": False,
    },
    10: {
        "titulo": "Introducción a la pintura",
        "autor": "Camila Torres",
        "genero": "arte",
        "anio_publicacion": 2020,
        "precio": "17.75",
        "ubicacion": "Estante D",
        "estado": "nuevo",
        "disponible": True,
    },
}

LIBROS_NUEVOS = [
    {
        "titulo": "El cielo nocturno",
        "autor": "Diego Luna",
        "genero": "astronomía",
        "anio_publicacion": 2022,
        "precio": "21.00",
        "ubicacion": "Estante E",
        "estado": "nuevo",
        "disponible": True,
    },
    {
        "titulo": "Fundamentos de programación",
        "autor": "Elena Castro",
        "genero": "tecnología",
        "anio_publicacion": 2024,
        "precio": "28.50",
        "ubicacion": "Estante F",
        "estado": "nuevo",
        "disponible": True,
    },
    {
        "titulo": "Historias del fútbol",
        "autor": "Pablo Díaz",
        "genero": "deportes",
        "anio_publicacion": 2019,
        "precio": "16.90",
        "ubicacion": "Estante G",
        "estado": "usado",
        "disponible": True,
    },
    {
        "titulo": "Animales de la selva",
        "autor": "Lucía Fernández",
        "genero": "naturaleza",
        "anio_publicacion": 2021,
        "precio": "14.00",
        "ubicacion": "Estante H",
        "estado": "nuevo",
        "disponible": False,
    },
    {
        "titulo": "Economía para principiantes",
        "autor": "Andrés Molina",
        "genero": "economía",
        "anio_publicacion": 2020,
        "precio": "23.25",
        "ubicacion": "Estante I",
        "estado": "nuevo",
        "disponible": True,
    },
    {
        "titulo": "Poemas para el camino",
        "autor": "Valeria Cruz",
        "genero": "poesía",
        "anio_publicacion": 2017,
        "precio": "12.50",
        "ubicacion": "Estante J",
        "estado": "usado",
        "disponible": True,
    },
]


def completar_libros(apps, schema_editor):
    Libro = apps.get_model("app_catalogo", "libro")
    manager = Libro.objects.using(schema_editor.connection.alias)
    for libro_id, datos in LIBROS_EXISTENTES.items():
        manager.filter(pk=libro_id).update(**datos)
    manager.bulk_create([Libro(**datos) for datos in LIBROS_NUEVOS])


class Migration(migrations.Migration):
    dependencies = [
        ("app_catalogo", "0004_agregar_libros"),
    ]

    operations = [
        migrations.RunPython(completar_libros, migrations.RunPython.noop),
    ]
