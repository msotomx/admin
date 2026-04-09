# En esta app se guardan los datos de las visitas que llegan a la pagina de registro

from django.db import models


class VisitaRegistro(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    ciudad = models.CharField(max_length=120, blank=True, default="")
    pais = models.CharField(max_length=120, blank=True, default="")
    user_agent = models.TextField(blank=True, default="")
    referrer = models.TextField(blank=True, default="")
    es_bot = models.BooleanField(default=False)
    path = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        ordering = ["-fecha_hora"]
        verbose_name = "Visita a registro"
        verbose_name_plural = "Visitas a registro"

    def __str__(self):
        return f"{self.fecha_hora} - {self.ip} - {self.ciudad or 'Sin ciudad'}"
    