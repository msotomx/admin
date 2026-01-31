from django.db import models

class ArticuloAyuda(models.Model):
    categoria = models.CharField(max_length=100)     # Ej: "Movimientos de Almacén"
    titulo = models.CharField(max_length=200)        # Ej: "Traspasos"
    slug = models.SlugField(max_length=220, unique=True)
    orden = models.PositiveIntegerField(default=0)
    contenido_html = models.TextField()              # HTML directo
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["categoria", "orden", "titulo"]

    def __str__(self):
        return f"{self.categoria} - {self.titulo}"
