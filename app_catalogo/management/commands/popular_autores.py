from datetime import date

from django.core.management.base import BaseCommand

from app_catalogo.models import autor, libro

AUTORES_DATOS = {
    "Ana Ruiz": {
        "nacionalidad": "España",
        "fecha_nacimiento": date(1990, 3, 12),
        "biografia": "Autora española especializada en libros de tecnología y programación para principiantes.",
    },
    "Andrés Molina": {
        "nacionalidad": "Colombia",
        "fecha_nacimiento": date(1978, 7, 4),
        "biografia": "Economista y escritor colombiano, autor de textos de divulgación económica.",
    },
    "Camila Torres": {
        "nacionalidad": "Chile",
        "fecha_nacimiento": date(1985, 11, 23),
        "biografia": "Artista y escritora chilena, autora de libros sobre pintura y técnicas artísticas.",
    },
    "Carlos Vega": {
        "nacionalidad": "México",
        "fecha_nacimiento": date(1975, 2, 18),
        "biografia": "Divulgador científico mexicano, autor de libros sobre astronomía y el universo.",
    },
    "Diego Luna": {
        "nacionalidad": "Argentina",
        "fecha_nacimiento": date(1982, 9, 5),
        "biografia": "Escritor argentino apasionado por la astronomía y el cielo nocturno.",
    },
    "Elena Castro": {
        "nacionalidad": "España",
        "fecha_nacimiento": date(1988, 5, 30),
        "biografia": "Programadora y autora española de libros introductorios de programación.",
    },
    "Ernesto Salas": {
        "nacionalidad": "Perú",
        "fecha_nacimiento": date(1965, 1, 15),
        "biografia": "Historiador peruano, autor de obras de divulgación histórica.",
    },
    "Gabriel García Márquez": {
        "nacionalidad": "Colombia",
        "fecha_nacimiento": date(1927, 3, 6),
        "biografia": "Escritor colombiano, Premio Nobel de Literatura 1982, autor de Cien años de soledad.",
    },
    "Julián Ortega": {
        "nacionalidad": "España",
        "fecha_nacimiento": date(1980, 6, 22),
        "biografia": "Novelista español, autor de relatos sobre la vida urbana y la lluvia.",
    },
    "Lucía Fernández": {
        "nacionalidad": "España",
        "fecha_nacimiento": date(1992, 8, 14),
        "biografia": "Escritora española especializada en literatura infantil y juvenil.",
    },
    "Marta Ríos": {
        "nacionalidad": "Colombia",
        "fecha_nacimiento": date(1970, 12, 1),
        "biografia": "Escritora colombiana, autora de novelas y cuentos ambientados en el río Magdalena.",
    },
    "Mojang Studios": {
        "nacionalidad": "Suecia",
        "fecha_nacimiento": date(2009, 5, 11),
        "biografia": "Estudio de videojuegos sueco, creador de Minecraft y sus guías oficiales.",
    },
    "Pablo Díaz": {
        "nacionalidad": "Uruguay",
        "fecha_nacimiento": date(1983, 10, 9),
        "biografia": "Periodista deportivo uruguayo, autor de libros sobre historia del fútbol.",
    },
    "Sofía Herrera": {
        "nacionalidad": "España",
        "fecha_nacimiento": date(1991, 4, 27),
        "biografia": "Chef y escritora española, autora de libros de cocina para todos los niveles.",
    },
    "Valeria Cruz": {
        "nacionalidad": "México",
        "fecha_nacimiento": date(1995, 7, 19),
        "biografia": "Poeta mexicana, autora de colecciones de poesía contemporánea.",
    },
}

DATOS_POR_DEFECTO = {
    "nacionalidad": "Desconocida",
    "fecha_nacimiento": date(1970, 1, 1),
    "biografia": "Biografía pendiente de completar.",
}


class Command(BaseCommand):
    help = (
        "Crea o actualiza en app_catalogo_autor un registro por cada autor "
        "distinto que ya aparece en los libros."
    )

    def handle(self, *args, **options):
        nombres = sorted(set(libro.objects.values_list("autor", flat=True)))
        creados = 0
        actualizados = 0

        for nombre in nombres:
            datos = AUTORES_DATOS.get(nombre, DATOS_POR_DEFECTO)
            autor_obj = autor.objects.filter(nombre=nombre).first()

            if autor_obj is None:
                autor.objects.create(
                    nombre=nombre,
                    biografia=datos["biografia"],
                    fecha_nacimiento=datos["fecha_nacimiento"],
                    nacionalidad=datos["nacionalidad"],
                )
                creados += 1
                self.stdout.write(self.style.SUCCESS(f"Creado: {nombre}"))
            else:
                autor_obj.biografia = datos["biografia"]
                autor_obj.fecha_nacimiento = datos["fecha_nacimiento"]
                autor_obj.nacionalidad = datos["nacionalidad"]
                autor_obj.save()
                actualizados += 1
                self.stdout.write(f"Actualizado: {nombre}")

        self.stdout.write(
            self.style.SUCCESS(f"Listo. {creados} creado(s), {actualizados} actualizado(s).")
        )
