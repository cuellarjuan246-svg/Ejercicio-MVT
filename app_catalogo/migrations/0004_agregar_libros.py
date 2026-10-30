from django.db import migrations


LIBROS = [
    {
        "titulo": "Aprender Django",
        "autor": "Laura Méndez",
        "genero": "tecnologia",
        "anio_publicacion": 2022,
        "precio": "29.90",
        "ubicacion": "Estante A",
        "estado": "nuevo",
        "disponible": True,
    },
    {
        "titulo": "Misterios del océano",
        "autor": "Carlos Vega",
        "genero": "ciencia",
        "anio_publicacion": 2019,
        "precio": "24.50",
        "ubicacion": "Estante B",
        "estado": "nuevo",
        "disponible": True,
    },
    {
        "titulo": "Historia de dos ciudades",
        "autor": "Ana Ruiz",
        "genero": "historia",
        "anio_publicacion": 2015,
        "precio": "18.00",
        "ubicacion": "Estante C",
        "estado": "usado",
        "disponible": False,
    },
    {
        "titulo": "El jardín secreto",
        "autor": "Marta Ríos",
        "genero": "infantil",
        "anio_publicacion": 2020,
        "precio": "15.75",
        "ubicacion": "Estante D",
        "estado": "nuevo",
        "disponible": True,
    },
]


def agregar_libros(apps, schema_editor):
    Libro = apps.get_model("app_catalogo", "libro")
    Libro.objects.using(schema_editor.connection.alias).bulk_create(
        [Libro(**libro) for libro in LIBROS]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("app_catalogo", "0003_usuario_editorial_tema_and_more"),
    ]

    operations = [
        migrations.RunPython(agregar_libros, migrations.RunPython.noop),
    ]
