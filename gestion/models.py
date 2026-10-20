from django.db import models
from django.core.validators import MinValueValidator
import uuid

class Recinto(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre del recinto",
    )
    direccion = models.CharField(max_length=200)
    capacidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Número máximo de personas",
    )
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Patrocinador(models.Model):
    nombre = models.CharField(max_length=100)
    cif = models.CharField(max_length=9, unique=True)
    aportacion = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sector = models.CharField(max_length=50, blank=True)
    web = models.URLField(blank=True)

    def __str__(self):
        return self.nombre
    
class Festival(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    aforo = models.PositiveIntegerField(default=1000)
    activo = models.BooleanField(default=True)

    recinto = models.OneToOneField(
        Recinto,
        on_delete=models.CASCADE,
        related_name="festival",
    )
    patrocinadores = models.ManyToManyField(
        Patrocinador,
        related_name="festivales",
        blank=True,
    )

    def __str__(self):
        return self.nombre