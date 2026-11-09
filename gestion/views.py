from django.http import Http404
from django.db.models import Prefetch, Q
from django.shortcuts import render, get_object_or_404
from .models import Festival, Actuacion, Entrada, Artista

def index(request):
    # Vista principal
    return render(request, 'gestion/index.html')

def lista_festivales(request):
    # Lista todos los festivales ordenados por fecha de inicio, mostrando
   
    festivales = (
        Festival.objects
        .select_related('recinto')
        .prefetch_related('patrocinadores', 'escenarios')
        .order_by('fecha_inicio')
    )
    return render(request, 'gestion/lista_festivales.html', {'festivales': festivales})

def detalle_festival(request, id):
    # Muestra un festival concreto (id entero recibido por la URL) con todos
    # sus datos relacionados: recinto (OneToOne), patrocinadores (ManyToMany),
    # escenarios (ManyToOne reversa), actuaciones con su artista y escenario
    # (ManyToMany con tabla intermedia Actuacion) y entradas con su asistente
    # (ManyToOne). Si el festival no existe, devuelve un error 404.
  
    #   -- 1) El festival con su recinto
    #   SELECT f.*, r.*
    #   FROM gestion_festival f
    #   INNER JOIN gestion_recinto r ON f.recinto_id = r.id
    #   WHERE f.id = <id>;
    #
    #   -- 2) Patrocinadores y 3) escenarios del festival (prefetch_related)
    #   SELECT p.* FROM gestion_patrocinador p
    #   INNER JOIN gestion_festival_patrocinadores fp ON p.id = fp.patrocinador_id
    #   WHERE fp.festival_id = <id>;
    #   SELECT e.* FROM gestion_escenario e WHERE e.festival_id = <id>;
    #
    #   -- 4) Actuaciones del festival con su artista y su escenario
    #   SELECT a.*, ar.*, e.*
    #   FROM gestion_actuacion a
    #   INNER JOIN gestion_artista ar ON a.artista_id = ar.id
    #   LEFT JOIN gestion_escenario e ON a.escenario_id = e.id
    #   WHERE a.festival_id = <id>
    #   ORDER BY a.fecha_hora ASC;
    #
    #   -- 5) Entradas del festival con su asistente
    # 
    festival = get_object_or_404(
        Festival.objects
        .select_related('recinto')
        .prefetch_related('patrocinadores', 'escenarios'),
        id=id,
    )
    actuaciones = (
        Actuacion.objects
        .select_related('artista', 'escenario')
        .filter(festival=festival)
        .order_by('fecha_hora')
    )
    entradas = (
        Entrada.objects
        .select_related('asistente')
        .filter(festival=festival)
        .order_by('fecha_compra')
    )
    contexto = {
        'festival': festival,
        'actuaciones': actuaciones,
        'entradas': entradas,
    }
    return render(request, 'gestion/detalle_festival.html', contexto)

def artistas_por_genero(request, genero):
    # Lista los artistas de un género musical (parámetro str de la URL) cuya
    # popularidad sea al menos 40 (filtro con AND), ordenados de más a menos
    # populares. Muestra su perfil (OneToOne), sus actuaciones con festival y
    # escenario (ManyToMany con tabla intermedia Actuacion) y los asistentes
    # que lo tienen como favorito (ManyToMany reversa). Si el género no
    # existe, devuelve un error 404.
    #

    #   -- 1) Artistas del género con popularidad >= 40 y su perfil

    #
    #   -- 2) Actuaciones de esos artistas con su festival y su escenario
    #
    #
    #   -- 3) Asistentes que tienen a esos artistas como favoritos

    generos_validos = dict(Artista.GENEROS)
    if genero not in generos_validos:
        raise Http404("Género no válido")

    artistas = (
        Artista.objects
        .select_related('perfil')
        .prefetch_related(
            Prefetch(
                'actuacion_set',
                queryset=Actuacion.objects
                .select_related('festival', 'escenario')
                .order_by('fecha_hora'),
            ),
            'seguidores',
        )
        .filter(genero=genero, popularidad__gte=40)
        .order_by('-popularidad')
    )
    contexto = {
        'artistas': artistas,
        'genero': generos_validos[genero],
    }
    return render(request, 'gestion/artistas_por_genero.html', contexto)


def entradas_festival(request, id, tipo):
    # Lista las entradas de un tipo concreto (general, vip o abono) vendidas
    # para un festival. Recibe dos parámetros por la URL: el id del festival
    # (entero) y el tipo de entrada (texto). Filtra con AND por festival y
    # tipo, y las ordena de más a menos caras. Para cada entrada muestra al
    # asistente (ManyToOne), su carnet (OneToOne reversa) y sus artistas
    # favoritos (ManyToMany). Si el festival o el tipo no existen, devuelve
    # un error 404.
    #
    # SQL equivalente (3 consultas):
    #   -- 1) El festival con su recinto
    #   -- 2) Entradas del tipo pedido con su asistente y el carnet
    #   -- 3) Artistas favoritos de esos asistentes
    
    tipos_validos = dict(Entrada.TIPOS)
    if tipo not in tipos_validos:
        raise Http404("Tipo de entrada no válido")

    festival = get_object_or_404(
        Festival.objects.select_related('recinto'),
        id=id,
    )
    entradas = (
        Entrada.objects
        .select_related('asistente', 'asistente__carnet')
        .prefetch_related('asistente__artistas_favoritos')
        .filter(festival=festival, tipo=tipo)
        .order_by('-precio')
    )
    contexto = {
        'festival': festival,
        'tipo': tipos_validos[tipo],
        'entradas': entradas,
    }
    return render(request, 'gestion/entradas_festival.html', contexto)

def festivales_por_anio(request, anio):
    # Lista los festivales que empiezan O terminan en el año indicado por la
    # URL (4 dígitos, validados con una expresión regular en re_path).
    # Usa un filtro con OR mediante Q y ordena por fecha de inicio. Muestra
    # el recinto (OneToOne), los patrocinadores (ManyToMany), los escenarios
    # (ManyToOne reversa) y las actuaciones con su artista y escenario
    # (ManyToMany con tabla intermedia Actuacion).
    #
    # SQL equivalente (4 consultas):
    #   -- 1) Festivales del año con su recinto (filtro OR)
    #   SELECT f.*, r.*
    #   FROM gestion_festival f
    #   INNER JOIN gestion_recinto r ON f.recinto_id = r.id
    #   WHERE f.fecha_inicio BETWEEN '<anio>-01-01' AND '<anio>-12-31'
    #      OR f.fecha_fin BETWEEN '<anio>-01-01' AND '<anio>-12-31'
    #   ORDER BY f.fecha_inicio ASC;
    #
    #   -- 2) Patrocinadores de esos festivales
    #   -- 3) Escenarios de esos festivales
    #   -- 4) Actuaciones con su artista y su escenario

    anio = int(anio)
    festivales = (
        Festival.objects
        .select_related('recinto')
        .prefetch_related(
            'patrocinadores',
            'escenarios',
            Prefetch(
                'actuacion_set',
                queryset=Actuacion.objects
                .select_related('artista', 'escenario')
                .order_by('fecha_hora'),
            ),
        )
        .filter(Q(fecha_inicio__year=anio) | Q(fecha_fin__year=anio))
        .order_by('fecha_inicio')
    )
    contexto = {
        'festivales': festivales,
        'añio': anio,
    }
    return render(request, 'gestion/festivales_por_anio.html', contexto)