from django.db import migrations


LIBROS = [
    {
        "id": 1,
        "titulo": "El río de las palabras",
        "autor": "Marta Ríos",
        "anio": 1998,
        "genero": "novela",
        "disponible": True,
    },
    {
        "id": 2,
        "titulo": "Noches de lluvia",
        "autor": "Julián Ortega",
        "anio": 2005,
        "genero": "novela",
        "disponible": True,
    },
    {
        "id": 3,
        "titulo": "Python desde cero",
        "autor": "Ana Ruiz",
        "anio": 2021,
        "genero": "tecnologia",
        "disponible": False,
    },
    {
        "id": 4,
        "titulo": "El universo en tu bolsillo",
        "autor": "Carlos Vega",
        "anio": 2012,
        "genero": "ciencia",
        "disponible": False,
    },
    {
        "id": 5,
        "titulo": "Cuentos del Magdalena",
        "autor": "Marta Ríos",
        "anio": 1987,
        "genero": "novela",
        "disponible": True,
    },
    {
        "id": 6,
        "titulo": "Cien años de soledad",
        "autor": "Gabriel García Márquez",
        "anio": 1967,
        "genero": "novela",
        "disponible": True,
    },
]


def cargar_libros(apps, schema_editor):
    Libro = apps.get_model("app_catalogo", "Libro")
    Libro.objects.using(schema_editor.connection.alias).bulk_create(
        [Libro(**libro) for libro in LIBROS],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("app_catalogo", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(cargar_libros, migrations.RunPython.noop),
    ]
