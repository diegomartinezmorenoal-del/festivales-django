from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from gestion.models import (
    Recinto, Patrocinador, Festival, Artista, PerfilArtista,
    Escenario, Actuacion, Asistente, CarnetAsistente, Entrada,
)


class Command(BaseCommand):
    help = "Rellena la base de datos con datos fijos de ejemplo"

    def handle(self, *args, **options):
        # Recintos
        recinto1, _ = Recinto.objects.get_or_create(
            nombre="Parque del Alamillo",
            defaults={
                "direccion": "Av. de los Descubrimientos, Sevilla",
                "capacidad": 20000,
                "latitud": 37.4237,
                "longitud": -6.0021,
            },
        )
        recinto2, _ = Recinto.objects.get_or_create(
            nombre="Estadio de la Cartuja",
            defaults={
                "direccion": "Isla de la Cartuja, Sevilla",
                "capacidad": 60000,
                "latitud": 37.4180,
                "longitud": -6.0080,
            },
        )

        # Patrocinadores
        pat1, _ = Patrocinador.objects.get_or_create(
            cif="A11111111",
            defaults={"nombre": "CervezaSur", "aportacion": 15000,
                      "sector": "Bebidas", "web": "https://cervezasur.example.com"},
        )
        pat2, _ = Patrocinador.objects.get_or_create(
            cif="B22222222",
            defaults={"nombre": "TeleAndalucia", "aportacion": 8000,
                      "sector": "Telecomunicaciones", "web": "https://teleandalucia.example.com"},
        )

        # Festivales (OneToOne con Recinto)
        hoy = date.today()
        fest1, _ = Festival.objects.get_or_create(
            nombre="Festival Giralda Sound",
            defaults={
                "descripcion": "Tres días de música en Sevilla",
                "fecha_inicio": hoy + timedelta(days=60),
                "fecha_fin": hoy + timedelta(days=62),
                "aforo": 20000,
                "recinto": recinto1,
            },
        )
        fest2, _ = Festival.objects.get_or_create(
            nombre="Cartuja Electro Fest",
            defaults={
                "descripcion": "Festival de música electrónica",
                "fecha_inicio": hoy + timedelta(days=90),
                "fecha_fin": hoy + timedelta(days=91),
                "aforo": 50000,
                "recinto": recinto2,
            },
        )
        fest1.patrocinadores.add(pat1, pat2)
        fest2.patrocinadores.add(pat1)

        # Artistas
        art1, _ = Artista.objects.get_or_create(
            nombre_artistico="Los Guadalquivires",
            defaults={"genero": "rock", "email": "guadalquivires@example.com",
                      "popularidad": 80, "fecha_formacion": date(2010, 5, 20)},
        )
        art2, _ = Artista.objects.get_or_create(
            nombre_artistico="DJ Triana",
            defaults={"genero": "electronica", "email": "djtriana@example.com",
                      "popularidad": 90, "fecha_formacion": date(2015, 3, 10)},
        )
        art3, _ = Artista.objects.get_or_create(
            nombre_artistico="Carmen Albero",
            defaults={"genero": "flamenco", "email": "carmen@example.com",
                      "popularidad": 70, "fecha_formacion": date(2008, 9, 1)},
        )

        # Perfiles (OneToOne con Artista)
        PerfilArtista.objects.get_or_create(
            artista=art1,
            defaults={"web": "https://guadalquivires.example.com",
                      "instagram": "@guadalquivires", "cache": 5000},
        )
        PerfilArtista.objects.get_or_create(
            artista=art2,
            defaults={"web": "https://djtriana.example.com",
                      "instagram": "@djtriana", "cache": 8000,
                      "contrato_exclusivo": True},
        )
        PerfilArtista.objects.get_or_create(
            artista=art3,
            defaults={"instagram": "@carmenalbero", "cache": 3500},
        )

        # Escenarios
        esc1, _ = Escenario.objects.get_or_create(
            nombre="Escenario Giralda", festival=fest1,
            defaults={"tipo": "principal", "capacidad": 15000},
        )
        esc2, _ = Escenario.objects.get_or_create(
            nombre="Carpa Triana", festival=fest1,
            defaults={"tipo": "carpa", "capacidad": 3000, "techado": True},
        )
        esc3, _ = Escenario.objects.get_or_create(
            nombre="Main Stage Cartuja", festival=fest2,
            defaults={"tipo": "principal", "capacidad": 40000},
        )

        # Actuaciones (tabla intermedia con atributos extra)
        ahora = timezone.now()
        Actuacion.objects.get_or_create(
            artista=art1, festival=fest1,
            defaults={"escenario": esc1,
                      "fecha_hora": ahora + timedelta(days=60, hours=4),
                      "duracion": timedelta(hours=1, minutes=30),
                      "cache_pactado": 5000},
        )
        Actuacion.objects.get_or_create(
            artista=art3, festival=fest1,
            defaults={"escenario": esc2,
                      "fecha_hora": ahora + timedelta(days=61, hours=2),
                      "duracion": timedelta(hours=1),
                      "cache_pactado": 3500},
        )
        Actuacion.objects.get_or_create(
            artista=art2, festival=fest2,
            defaults={"escenario": esc3,
                      "fecha_hora": ahora + timedelta(days=90, hours=6),
                      "duracion": timedelta(hours=2),
                      "cache_pactado": 8000},
        )

        # Asistentes
        asis1, _ = Asistente.objects.get_or_create(
            email="lucia@example.com",
            defaults={"nombre": "Lucía", "apellidos": "Pérez Gómez",
                      "fecha_nacimiento": date(1998, 4, 12),
                      "telefono": "600111222"},
        )
        asis2, _ = Asistente.objects.get_or_create(
            email="pablo@example.com",
            defaults={"nombre": "Pablo", "apellidos": "Ruiz Soto",
                      "fecha_nacimiento": date(1995, 11, 3)},
        )
        asis1.artistas_favoritos.add(art1, art2)
        asis2.artistas_favoritos.add(art3)

        # Carnets (OneToOne con Asistente)
        CarnetAsistente.objects.get_or_create(asistente=asis1, defaults={"puntos": 120})
        CarnetAsistente.objects.get_or_create(asistente=asis2, defaults={"puntos": 30})

        # Entradas
        Entrada.objects.get_or_create(
            codigo="ENT-0001",
            defaults={"tipo": "vip", "precio": 150,
                      "asistente": asis1, "festival": fest1},
        )
        Entrada.objects.get_or_create(
            codigo="ENT-0002",
            defaults={"tipo": "general", "precio": 60,
                      "asistente": asis2, "festival": fest1},
        )
        Entrada.objects.get_or_create(
            codigo="ENT-0003",
            defaults={"tipo": "abono", "precio": 90,
                      "asistente": asis1, "festival": fest2},
        )

        self.stdout.write(self.style.SUCCESS("Seeders ejecutados correctamente"))