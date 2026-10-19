from unittest.mock import patch

from django.test import TestCase


class InicioViewTests(TestCase):
    def test_muestra_cantidad_de_libros_disponibles_y_prestados(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 6)
        self.assertEqual(response.context["libros_disponibles"], 4)
        self.assertEqual(response.context["libros_prestados"], 2)
        self.assertContains(response, "Tenemos 6 libros en el catálogo.")
        self.assertContains(response, "Libros disponibles: 4")
        self.assertContains(response, "Libros prestados: 2")
        self.assertNotContains(response, "¡Todos los libros están en la biblioteca!")

    @patch("app_catalogo.views.LIBROS", [
        {"titulo": "Libro de ejemplo", "disponible": True},
    ])
    def test_muestra_mensaje_si_no_hay_libros_prestados(self):
        response = self.client.get("/")

        self.assertContains(response, "¡Todos los libros están en la biblioteca!")

    def test_filtra_libros_por_genero(self):
        response = self.client.get("/libros/?genero=novela")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["libros"]), 3)
        self.assertContains(response, "Cuentos del Magdalena")
        self.assertNotContains(response, "Python desde cero")

    def test_genero_sin_resultados_muestra_mensaje(self):
        response = self.client.get("/libros/?genero=poesia")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay libros de ese género.")

    def test_detalle_de_libro_y_404_para_id_inexistente(self):
        response = self.client.get("/libros/3/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python desde cero")
        self.assertEqual(self.client.get("/libros/99/").status_code, 404)

    def test_pagina_acerca_muestra_version(self):
        response = self.client.get("/acerca/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Versión 1.0")

    def test_autores_sin_repetir_ordenados_y_con_cantidad(self):
        response = self.client.get("/autores/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["autores"],
            [
                {"nombre": "Ana Ruiz", "cantidad_libros": 1},
                {"nombre": "Carlos Vega", "cantidad_libros": 1},
                {"nombre": "Julián Ortega", "cantidad_libros": 1},
                {"nombre": "Laura Méndez", "cantidad_libros": 1},
                {"nombre": "Marta Ríos", "cantidad_libros": 2},
            ],
        )
        self.assertContains(response, "Marta Ríos: 2 libros")

    def test_logica_muestra_conteos_porcentaje_y_generos(self):
        response = self.client.get("/logica/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 6)
        self.assertEqual(response.context["disponibles"], 4)
        self.assertEqual(response.context["prestados"], 2)
        self.assertEqual(response.context["porcentaje_disponible"], 67)
        self.assertEqual(
            response.context["libros_por_genero"],
            [
                {"genero": "ciencia", "cantidad": 1},
                {"genero": "novela", "cantidad": 3},
                {"genero": "tecnologia", "cantidad": 2},
            ],
        )
        self.assertContains(response, "Porcentaje disponible: 67%")
        self.assertNotContains(response, "Advertencia:")

    @patch("app_catalogo.views.LIBROS", [
        {"genero": "novela", "disponible": False},
        {"genero": "ciencia", "disponible": True},
        {"genero": "novela", "disponible": False},
    ])
    def test_logica_muestra_advertencia_si_porcentaje_es_menor_a_50(self):
        response = self.client.get("/logica/")

        self.assertEqual(response.context["porcentaje_disponible"], 33)
        self.assertContains(response, "Advertencia:")

    @patch("app_catalogo.views.LIBROS", [])
    def test_logica_con_catalogo_vacio_evitan_division_por_cero(self):
        response = self.client.get("/logica/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["porcentaje_disponible"], 0)
        self.assertContains(response, "No hay libros en el catálogo.")
        self.assertContains(response, "Advertencia:")

    def test_sugerencia_muestra_confirmacion_con_titulo(self):
        response = self.client.post("/sugerir/", {"titulo": "Un libro nuevo"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gracias, tendremos en cuenta: Un libro nuevo")

    def test_sugerencia_vacia_muestra_error(self):
        response = self.client.post("/sugerir/", {"titulo": "   "})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Escribe un título")

    def test_formulario_sugerencia_incluye_proteccion_csrf(self):
        response = self.client.get("/sugerir/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_rutas_de_ejercicios_anteriores_siguen_funcionando(self):
        self.assertContains(self.client.get("/hola/"), "Hola desde Django")
        self.assertContains(self.client.get("/cuadrado/7/"), "El cuadrado de 7 es 49")
        self.assertContains(self.client.get("/contacto/"), "Contacto")
