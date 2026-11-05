import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    SQLite no permite un ALTER normal aquí: la tabla autor cambia su columna
    primaria de "id_id" (OneToOneField a usuario) a "id" (AutoField propio),
    y publicacion.autor_id referencia esa columna por nombre. Se reconstruyen
    ambas tablas a mano (estaban vacías) para evitar el "foreign key mismatch"
    que lanza el ALTER automático de Django en SQLite.
    """

    atomic = False

    dependencies = [
        ('app_catalogo', '0008_usuario_numero_documento_usuario_telefono_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=[
                        "PRAGMA foreign_keys=OFF;",
                        "DROP TABLE app_catalogo_publicacion;",
                        "DROP TABLE app_catalogo_autor;",
                        (
                            'CREATE TABLE "app_catalogo_autor" ('
                            '"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, '
                            '"nombre" varchar(100) NOT NULL, '
                            '"biografia" text NOT NULL, '
                            '"fecha_nacimiento" date NOT NULL, '
                            '"nacionalidad" varchar(50) NOT NULL)'
                        ),
                        (
                            'CREATE TABLE "app_catalogo_publicacion" ('
                            '"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, '
                            '"fecha_publicacion" date NOT NULL, '
                            '"resumen" text NOT NULL, '
                            '"titulo" varchar(200) NOT NULL, '
                            '"edicion" varchar(50) NOT NULL, '
                            '"ISBN" varchar(20) NOT NULL UNIQUE, '
                            '"editorial_id" integer NULL REFERENCES "app_catalogo_editorial" ("id") DEFERRABLE INITIALLY DEFERRED, '
                            '"libro_id" integer NOT NULL REFERENCES "app_catalogo_libro" ("id") DEFERRABLE INITIALLY DEFERRED, '
                            '"tema_id" integer NOT NULL REFERENCES "app_catalogo_tema" ("id") DEFERRABLE INITIALLY DEFERRED, '
                            '"autor_id" integer NOT NULL REFERENCES "app_catalogo_autor" ("id") DEFERRABLE INITIALLY DEFERRED)'
                        ),
                        "PRAGMA foreign_keys=ON;",
                    ],
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='autor',
                    name='id',
                    field=models.AutoField(primary_key=True, serialize=False),
                ),
                migrations.AlterField(
                    model_name='publicacion',
                    name='autor',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_catalogo.autor'),
                ),
            ],
        ),
    ]
