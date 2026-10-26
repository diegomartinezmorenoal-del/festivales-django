
from django.contrib import admin
from .models import (
    Recinto,
    Patrocinador,
    Festival,
    Artista,
    PerfilArtista,
    Escenario,
    Actuacion,
    Asistente,
    CarnetAsistente,
    Entrada,
)

admin.site.register(Recinto)
admin.site.register(Patrocinador)
admin.site.register(Festival)
admin.site.register(Artista)
admin.site.register(PerfilArtista)
admin.site.register(Escenario)
admin.site.register(Actuacion)
admin.site.register(Asistente)
admin.site.register(CarnetAsistente)
admin.site.register(Entrada)
