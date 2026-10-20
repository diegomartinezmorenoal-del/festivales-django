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

class Artista(models.Model):
    GENEROS = [
        ("rock", "Rock"),
        ("pop", "Pop"),
        ("electronica", "Electrónica"),
        ("hiphop", "Hip hop"),
        ("flamenco", "Flamenco"),
        ("otro", "Otro"),
    ]

    nombre_artistico = models.CharField(max_length=100, unique=True)
    genero = models.CharField(max_length=20, choices=GENEROS, default="otro")
    biografia = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    popularidad = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    fecha_formacion = models.DateField(null=True, blank=True)

    festivales = models.ManyToManyField(
        Festival,
        through="Actuacion",
        related_name="artistas",
    )

    def __str__(self):
        return self.nombre_artistico
 
class PerfilArtista(models.Model):
    artista = models.OneToOneField(
        Artista,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    web = models.URLField(blank=True)
    instagram = models.CharField(max_length=50, blank=True)
    cache = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contrato_exclusivo = models.BooleanField(default=False)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Perfil de {self.artista.nombre_artistico}"
class Escenario(models.Model):
    TIPOS = [
        ("principal", "Principal"),
        ("secundario", "Secundario"),
        ("carpa", "Carpa"),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS, default="secundario")
    capacidad = models.PositiveIntegerField(default=500)
    techado = models.BooleanField(default=False)

    festival = models.ForeignKey(
        Festival,
        on_delete=models.CASCADE,
        related_name="escenarios",
    )

    def __str__(self):
        return f"{self.nombre} ({self.festival.nombre})"

class Actuacion(models.Model):
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    escenario = models.ForeignKey(
        Escenario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actuaciones",
    )

    fecha_hora = models.DateTimeField()
    duracion = models.DurationField(help_text="Formato: HH:MM:SS")
    cache_pactado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cancelada = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Actuaciones"

    def __str__(self):
        return f"{self.artista} en {self.festival}"    
    
    