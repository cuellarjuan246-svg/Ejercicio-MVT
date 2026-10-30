LIBROS = [
    { "id": 1, "titulo": "El río de las palabras", "autor": "Marta Ríos", "anio": 1998, "genero": "novela", "disponible": True,},
    { "id": 2, "titulo": "Noches de lluvia", "autor": "Julián Ortega", "anio": 2005, "genero": "novela", "disponible": True,},
    { "id": 3, "titulo": "Python desde cero", "autor": "Ana Ruiz", "anio": 2021, "genero": "tecnologia", "disponible": False,},
    { "id": 4, "titulo": "El universo en tu bolsillo", "autor": "Carlos Vega", "anio": 2012, "genero": "ciencia", "disponible": False, },
    { "id": 5, "titulo": "Cuentos del Magdalena", "autor": "Marta Ríos", "anio": 1987, "genero": "novela", "disponible": True,},
    { "id": 6, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "anio": 1967, "genero": "novela", "disponible": True,},
]


def buscar_libro(libro_id):
    """Devuelve el libro con ese ID o None si no existe."""
    for libro in LIBROS:
        if libro["id"] == libro_id:
            return libro
    return None
