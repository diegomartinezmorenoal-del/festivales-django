import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from gestion.models import (
    Recinto, Patrocinador, Festival, Artista, PerfilArtista,
    Escenario, Actuacion, Asistente, CarnetAsistente, Entrada,
)


class Command(BaseCommand):
    help = "Genera datos aleatorios con Faker para cada modelo"

    def add_arguments(self, parser):
        parser.add_argument(
            "--cantidad",
            type=int,
            default=10,
            help="Número de registros a crear por modelo (por defecto 10)",
        )

    def handle(self, *args, **options):
        n = options["cantidad"]
        fake = Faker("es_ES")
        zona = timezone.get_current_timezone()

        # 1. Modelos sin dependencias: Recinto y Patrocinador
        recintos = []
        for _ in range(n):
            recintos.append(Recinto.objects.create(
                nombre=f"Recinto {fake.city()} {fake.numerify('###')}",
                direccion=fake.address().replace("\n", ", "),
                capacidad=random.randint(500, 60000),
                latitud=float(fake.latitude()),
                longitud=float(fake.longitude()),
            ))

        patrocinadores = []
        for _ in range(n):
            patrocinadores.append(Patrocinador.objects.create(
                nombre=fake.company(),
                cif=fake.bothify("?########", letters="ABCDEFGHJNPQRSUVW"),
                aportacion=random.randint(1000, 50000),
                sector=fake.job()[:50],
                web=fake.url(),
            ))

        # 2. Festival 
        festivales = []
        for recinto in recintos:
            inicio = fake.date_between(start_date="+10d", end_date="+180d")
            festival = Festival.objects.create(
                nombre=f"Festival {fake.word().capitalize()}",
                descripcion=fake.paragraph(),
                fecha_inicio=inicio,
                fecha_fin=inicio + timedelta(days=random.randint(1, 3)),
                aforo=random.randint(500, recinto.capacidad),
                activo=random.choice([True, False]),
                recinto=recinto,
            )
            festival.patrocinadores.set(
                random.sample(patrocinadores, k=random.randint(1, min(3, n)))
            )
            festivales.append(festival)

        # 3. 
        artistas = []
        for _ in range(n):
            artista = Artista.objects.create(
                nombre_artistico=f"{fake.word().capitalize()} {fake.last_name()} {fake.numerify('##')}",
                genero=random.choice([g[0] for g in Artista.GENEROS]),
                biografia=fake.paragraph(),
                email=fake.email(),
                popularidad=random.randint(0, 100),
                fecha_formacion=fake.date_between(start_date="-30y", end_date="-1y"),
            )
            PerfilArtista.objects.create(
                artista=artista,
                web=fake.url(),
                instagram="@" + fake.user_name()[:40],
                cache=random.randint(1000, 20000),
                contrato_exclusivo=random.choice([True, False]),
            )
            artistas.append(artista)

        # 4. Escenario 
        escenarios = []
        for _ in range(n):
            escenarios.append(Escenario.objects.create(
                nombre=f"Escenario {fake.word().capitalize()}",
                tipo=random.choice([t[0] for t in Escenario.TIPOS]),
                capacidad=random.randint(200, 20000),
                techado=random.choice([True, False]),
                festival=random.choice(festivales),
            ))

        # 5. Actuacion 
        for _ in range(n):
            escenario = random.choice(escenarios)
            Actuacion.objects.create(
                artista=random.choice(artistas),
                festival=escenario.festival,
                escenario=escenario,
                fecha_hora=fake.date_time_between(
                    start_date="+10d", end_date="+180d", tzinfo=zona
                ),
                duracion=timedelta(minutes=random.choice([45, 60, 90, 120])),
                cache_pactado=random.randint(1000, 20000),
                cancelada=random.choice([True, False]),
            )

        # 6. Asistente y CarnetAsistente 
        asistentes = []
        for _ in range(n):
            asistente = Asistente.objects.create(
                nombre=fake.first_name(),
                apellidos=fake.last_name() + " " + fake.last_name(),
                email=fake.unique.email(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=16, maximum_age=70),
                telefono=fake.numerify("6########"),
            )
            asistente.artistas_favoritos.set(
                random.sample(artistas, k=random.randint(1, min(3, n)))
            )
            CarnetAsistente.objects.create(
                asistente=asistente,
                puntos=random.randint(0, 500),
                activo=random.choice([True, False]),
            )
            asistentes.append(asistente)

        # 7. Entrada 
        for _ in range(n):
            Entrada.objects.create(
                tipo=random.choice([t[0] for t in Entrada.TIPOS]),
                precio=random.randint(30, 200),
                codigo="ENT-" + fake.unique.numerify("########"),
                usada=random.choice([True, False]),
                asistente=random.choice(asistentes),
                festival=random.choice(festivales),
            )

        self.stdout.write(self.style.SUCCESS(
            f"Datos aleatorios creados: {n} registros por modelo"
        ))