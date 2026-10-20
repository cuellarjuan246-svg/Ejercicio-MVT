from django.db import models


class usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10, choices=[("M", "Masculino"), ("F", "Femenino")])
    rol = models.CharField(max_length=20, choices=[("admin", "Administrador"), ("usuario", "Usuario")], default="usuario")

    def _str_(self):
        return self.nombre


class editorial(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)

    def _str_(self):
        return self.nombre

class tema(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def _str_(self):
        return self.nombre

class estudiante(models.Model):
    id = models.OneToOneField(usuario, on_delete=models.CASCADE, primary_key=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    grado_escolar = models.CharField(max_length=50)


    def _str_(self):
        return self.estudiante.nombre

class autor(models.Model):
    id = models.OneToOneField(usuario, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(max_length=100)
    biografia = models.TextField()
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=50)

    def _str_(self):
        return self.nombre


class libro(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    anio_publicacion = models.IntegerField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    ubicacion = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=[("nuevo", "Nuevo"), ("usado", "Usado")], default="nuevo")
    disponible = models.BooleanField(default=True)
    editorial = models.ForeignKey(editorial, on_delete=models.CASCADE, null=True, blank=True)
    tema = models.ForeignKey(tema, on_delete=models.CASCADE, null=True, blank=True)

    def _str_(self):
        return self.titulo


class prestamo(models.Model):
    id = models.AutoField(primary_key=True)
    observaciones = models.TextField(blank=True)
    libro = models.ForeignKey(libro, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(estudiante, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)

    def _str_(self):
        return f"Prestamo de {self.libro.titulo} a {self.estudiante.id.nombre}"

class publicacion(models.Model):
    id = models.AutoField(primary_key=True)
    libro = models.ForeignKey(libro, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()
    resumen = models.TextField()
    titulo = models.CharField(max_length=200)
    edicion = models.CharField(max_length=50)
    ISBN = models.CharField(max_length=20, unique=True)
    autor = models.ForeignKey(autor, on_delete=models.CASCADE)
    editorial = models.ForeignKey(editorial, on_delete=models.CASCADE, null=True, blank=True)
    tema = models.ForeignKey(tema, on_delete=models.CASCADE)

    def _str_(self):
        return f"Publicación de {self.libro.titulo} en {self.fecha_publicacion}"