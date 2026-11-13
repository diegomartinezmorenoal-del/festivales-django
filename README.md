# Festivales Django

Plataforma web para la **gestión de festivales de música**. Permite administrar festivales, recintos, artistas, escenarios, actuaciones, patrocinadores, asistentes, carnets y entradas.

## Índice

1. [Instalación y puesta en marcha](#1-instalación-y-puesta-en-marcha)
2. [Estructura de ramas de Git](#2-estructura-de-ramas-de-git)
3. [Archivos que no se suben a Git](#3-archivos-que-no-se-suben-a-git)
4. [Modelos, atributos y parámetros](#4-modelos-atributos-y-parámetros)
5. [Relaciones entre modelos](#5-relaciones-entre-modelos)
6. [Tipos de campo usados](#6-tipos-de-campo-usados)
7. [Parámetros usados](#7-parámetros-usados)
8. [Esquema entidad-relación](#8-esquema-entidad-relación)
9. [Seeders](#9-seeders)
10. [Comando con Faker](#10-comando-con-faker)
11. [Backup y fixtures](#11-backup-y-fixtures)
12. [Código no visto en clase (modelos, comandos y fixtures)](#12-código-no-visto-en-clase-modelos-comandos-y-fixtures)
13. [URLs y vistas](#13-urls-y-vistas)
14. [Páginas de error y modo producción](#14-páginas-de-error-y-modo-producción)
15. [Cómo probar el proyecto](#15-cómo-probar-el-proyecto)
16. [Código no visto en clase (URLs y vistas)](#16-código-no-visto-en-clase-urls-y-vistas)

---

## 1. Instalación y puesta en marcha

```bash
git clone <URL-del-repositorio>
cd festivales-django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py loaddata gestion/fixtures/datos_pruebas.json
python3 manage.py runserver
```

Los pasos para probar el proyecto, con más detalle, están en la [sección 15](#15-cómo-probar-el-proyecto).

- `python3 -m venv venv`: crea un entorno virtual aislado para las librerías del proyecto.
- `source venv/bin/activate`: activa ese entorno.
- `pip install -r requirements.txt`: instala las dependencias guardadas con sus versiones.
- `pip freeze > requirements.txt`: guarda las dependencias instaladas (se usó para generar el archivo).
- `django-admin startproject festivales .`: crea el proyecto en la carpeta actual. El punto final evita una carpeta duplicada `festivales/festivales/`.
- `python3 manage.py startapp gestion`: crea la aplicación `gestion`, donde están los modelos y las vistas.
- `python3 manage.py makemigrations`: genera los archivos de migración con las instrucciones para crear o modificar las tablas.
- `python3 manage.py migrate`: ejecuta las migraciones sobre la base de datos (`db.sqlite3`).
- `python3 manage.py check`: revisa el proyecto y avisa de errores sin ejecutarlo.
- `python3 manage.py runserver`: arranca el servidor de desarrollo en `http://127.0.0.1:8000/`.

La aplicación `gestion` está registrada en `INSTALLED_APPS` dentro de `festivales/settings.py`.

### Comandos propios del proyecto

| Comando | Qué hace |
|---|---|
| `python3 manage.py seeders` | Rellena la base de datos con datos fijos de ejemplo. |
| `python3 manage.py poblar` | Genera 10 registros aleatorios de cada modelo con Faker. |
| `python3 manage.py poblar --cantidad N` | Igual, pero con `N` registros por modelo. |
| `python3 manage.py dumpdata gestion --indent 2 --output gestion/fixtures/backup.json` | Crea el backup de los datos. |
| `python3 manage.py loaddata gestion/fixtures/datos_pruebas.json` | Carga los datos de pruebas. |

---

## 2. Estructura de ramas de Git

| Rama | Contenido |
|---|---|
| `main` | Rama principal. Contiene el proyecto completo, resultado de fusionar todas las demás. |
| `Configuracion_inicial` | Proyecto Django, entorno y `requirements.txt`. |
| `Modelos` | Modelos, migraciones, esquema E-R, seeders y comando Faker. |
| `Backups` | Todo lo anterior más la copia de seguridad de los datos (fixture). |
| `Vistas` | Rama de la tarea de URLs y vistas. Reúne todas las ramas de URL. |
| `url_festivales` | URL 2: lista de festivales. |
| `url_detalle_festival` | URL 3: detalle de un festival. |
| `url_artistas_genero` | URL 4: artistas por género. |
| `url_entradas_festival` | URL 5: entradas de un festival. |
| `url_festivales_anio` | URL 6: festivales por año. |
| `url_top_artistas` | URL 7: artistas más populares. |
| `url_estadisticas_entradas` | URL 8: estadísticas de entradas. |
| `url_actuaciones_sin_escenario` | URL 9: actuaciones sin escenario. |
| `url_asistentes` | URL 10: lista de asistentes. |
| `errores_personalizados` | Páginas de error 400, 403, 404 y 500. |
| `produccion_fixtures` | Modo producción y fixture de pruebas. |

Cada rama de URL se fusionó en `Vistas`, y `Vistas` se fusionó en `main` al terminar.

---

## 3. Archivos que no se suben a Git

Se excluyen con `.gitignore`:

| Entrada | Motivo |
|---|---|
| `venv/`, `.venv/`, `env/` | El entorno virtual pesa mucho y se recrea con `requirements.txt`. |
| `__pycache__/`, `*.pyc`, `*.pyo` | Archivos compilados que genera Python solos. |
| `db.sqlite3` | Base de datos local, que cada uno genera con `migrate`. |
| `.env` | Variables de entorno y datos sensibles. |
| `.idea/`, `.vscode/` | Configuración personal del editor. |
| `.DS_Store`, `Thumbs.db` | Archivos basura del sistema operativo. |

La carpeta `gestion/migrations/` **sí** se sube, porque define la estructura de la base de datos.

---

## 4. Modelos, atributos y parámetros

El proyecto tiene **10 modelos**, definidos en `gestion/models.py`. En cada tabla, la columna *Parámetros* indica qué opciones se han usado en el campo.

### 4.1 Recinto

Lugar físico donde se celebra un festival.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `nombre` | CharField | `max_length=100`, `unique=True`, `verbose_name` | Nombre del recinto, sin repetirse. |
| `direccion` | CharField | `max_length=200` | Dirección postal. |
| `capacidad` | PositiveIntegerField | `validators=[MinValueValidator(1)]`, `help_text` | Número máximo de personas. |
| `latitud` | FloatField | `null=True`, `blank=True` | Coordenada geográfica opcional. |
| `longitud` | FloatField | `null=True`, `blank=True` | Coordenada geográfica opcional. |

### 4.2 Patrocinador

Empresa que financia festivales.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `nombre` | CharField | `max_length=100` | Nombre de la empresa. |
| `cif` | CharField | `max_length=9`, `unique=True` | Identificación fiscal única. |
| `aportacion` | DecimalField | `max_digits=10`, `decimal_places=2`, `default=0` | Dinero aportado. |
| `sector` | CharField | `max_length=50`, `blank=True` | Sector de la empresa. |
| `web` | URLField | `blank=True` | Página web. |

### 4.3 Festival

Evento principal del proyecto.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `nombre` | CharField | `max_length=100` | Nombre del festival. |
| `descripcion` | TextField | `blank=True` | Texto largo descriptivo. |
| `fecha_inicio` | DateField | — | Primer día. |
| `fecha_fin` | DateField | — | Último día. |
| `aforo` | PositiveIntegerField | `default=1000` | Aforo total. |
| `activo` | BooleanField | `default=True` | Si el festival está vigente. |
| `recinto` | OneToOneField | `on_delete=CASCADE`, `related_name="festival"` | Recinto donde se celebra. |
| `patrocinadores` | ManyToManyField | `related_name="festivales"`, `blank=True` | Empresas que lo patrocinan. |

### 4.4 Artista

Músico o grupo que actúa en los festivales.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `nombre_artistico` | CharField | `max_length=100`, `unique=True` | Nombre artístico único. |
| `genero` | CharField | `max_length=20`, `choices=GENEROS`, `default="otro"` | Género musical (rock, pop, electrónica, hip hop, flamenco, otro). |
| `biografia` | TextField | `blank=True` | Biografía. |
| `email` | EmailField | `blank=True` | Correo de contacto. |
| `popularidad` | PositiveIntegerField | `default=0`, `validators=[MinValueValidator(0)]` | Puntuación de popularidad. |
| `fecha_formacion` | DateField | `null=True`, `blank=True` | Fecha de formación del artista o grupo. |
| `festivales` | ManyToManyField | `through="Actuacion"`, `related_name="artistas"` | Festivales en los que actúa. |

### 4.5 PerfilArtista

Datos profesionales ampliados de cada artista.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `artista` | OneToOneField | `on_delete=CASCADE`, `related_name="perfil"` | Artista al que pertenece. |
| `web` | URLField | `blank=True` | Web oficial. |
| `instagram` | CharField | `max_length=50`, `blank=True` | Usuario de Instagram. |
| `cache` | DecimalField | `max_digits=10`, `decimal_places=2`, `default=0` | Caché habitual. |
| `contrato_exclusivo` | BooleanField | `default=False` | Si tiene contrato de exclusividad. |
| `fecha_alta` | DateTimeField | `auto_now_add=True` | Fecha y hora de creación del perfil. |

### 4.6 Escenario

Escenario dentro de un festival.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `nombre` | CharField | `max_length=100` | Nombre del escenario. |
| `tipo` | CharField | `max_length=20`, `choices=TIPOS`, `default="secundario"` | Principal, secundario o carpa. |
| `capacidad` | PositiveIntegerField | `default=500` | Personas que caben. |
| `techado` | BooleanField | `default=False` | Si está cubierto. |
| `festival` | ForeignKey | `on_delete=CASCADE`, `related_name="escenarios"` | Festival al que pertenece. |

### 4.7 Actuacion (tabla intermedia)

Participación de un artista en un festival. Es la tabla intermedia (`through`) de la relación ManyToMany entre `Artista` y `Festival`.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `artista` | ForeignKey | `on_delete=CASCADE` | Artista que actúa. |
| `festival` | ForeignKey | `on_delete=CASCADE` | Festival donde actúa. |
| `escenario` | ForeignKey | `on_delete=SET_NULL`, `null=True`, `blank=True`, `related_name="actuaciones"` | Escenario asignado. |
| `fecha_hora` | DateTimeField | — | Cuándo actúa. |
| `duracion` | DurationField | `help_text="Formato: HH:MM:SS"` | Duración de la actuación. |
| `cache_pactado` | DecimalField | `max_digits=10`, `decimal_places=2`, `default=0` | Lo que cobra en ese festival. |
| `cancelada` | BooleanField | `default=False` | Si se ha cancelado. |

`class Meta` con `verbose_name_plural = "Actuaciones"`.

### 4.8 Asistente

Persona que compra entradas.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `nombre` | CharField | `max_length=50` | Nombre. |
| `apellidos` | CharField | `max_length=100` | Apellidos. |
| `email` | EmailField | `unique=True` | Correo único. |
| `fecha_nacimiento` | DateField | — | Fecha de nacimiento. |
| `telefono` | CharField | `max_length=15`, `blank=True` | Teléfono. |
| `artistas_favoritos` | ManyToManyField | `related_name="seguidores"`, `blank=True` | Artistas que sigue. |

### 4.9 CarnetAsistente

Carnet de fidelización de cada asistente.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `asistente` | OneToOneField | `on_delete=CASCADE`, `related_name="carnet"` | Dueño del carnet. |
| `codigo` | UUIDField | `default=uuid.uuid4`, `unique=True`, `editable=False` | Identificador único generado automáticamente. |
| `fecha_emision` | DateTimeField | `auto_now_add=True` | Fecha de emisión. |
| `puntos` | PositiveIntegerField | `default=0` | Puntos acumulados. |
| `activo` | BooleanField | `default=True` | Si el carnet está vigente. |

### 4.10 Entrada

Entrada comprada por un asistente para un festival.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `tipo` | CharField | `max_length=20`, `choices=TIPOS`, `default="general"` | General, VIP o abono. |
| `precio` | DecimalField | `max_digits=8`, `decimal_places=2` | Precio pagado. |
| `codigo` | CharField | `max_length=20`, `unique=True` | Código único de la entrada. |
| `fecha_compra` | DateTimeField | `auto_now_add=True` | Fecha y hora de compra. |
| `usada` | BooleanField | `default=False` | Si ya se ha usado. |
| `asistente` | ForeignKey | `on_delete=CASCADE`, `related_name="entradas"` | Quién la compró. |
| `festival` | ForeignKey | `on_delete=CASCADE`, `related_name="entradas"` | Festival al que da acceso. |

> Todos los métodos `__str__` devuelven un texto legible del objeto (por ejemplo el nombre) para que se vea bien en el admin y en el shell.

---

## 5. Relaciones entre modelos

El proyecto cumple los requisitos de relaciones. Todas están definidas en `gestion/models.py`.

### Relaciones OneToOne (3)

Enlazan un registro con **un único** registro de otro modelo, con `OneToOneField`.

| Modelo origen | Modelo destino | Campo | Descripción |
|---|---|---|---|
| `Festival` | `Recinto` | `recinto` | Cada festival se celebra en un único recinto, y cada recinto tiene un único festival asociado. |
| `PerfilArtista` | `Artista` | `artista` | Cada artista tiene un único perfil profesional. |
| `CarnetAsistente` | `Asistente` | `asistente` | Cada asistente tiene un único carnet. |

### Relaciones ManyToOne (4)

Muchos registros apuntan a **un** registro de otro modelo, con `ForeignKey`.

| Modelo origen (muchos) | Modelo destino (uno) | Campo | Descripción |
|---|---|---|---|
| `Escenario` | `Festival` | `festival` | Un festival tiene varios escenarios. |
| `Entrada` | `Asistente` | `asistente` | Un asistente puede comprar varias entradas. |
| `Entrada` | `Festival` | `festival` | Un festival vende muchas entradas. |
| `Actuacion` | `Escenario` | `escenario` | Un escenario acoge muchas actuaciones. |

### Relaciones ManyToMany (3)

Muchos registros se relacionan con muchos, con `ManyToManyField`.

| Modelo origen | Modelo destino | Campo | Tabla intermedia |
|---|---|---|---|
| `Artista` | `Festival` | `festivales` | **Manual**: `Actuacion`, con atributos extra. |
| `Festival` | `Patrocinador` | `patrocinadores` | Automática, creada por Django. |
| `Asistente` | `Artista` | `artistas_favoritos` | Automática, creada por Django. |

### ManyToMany con tabla intermedia y atributos extra

La relación entre `Artista` y `Festival` usa `through="Actuacion"`. Esa tabla no solo une los dos modelos con sus `ForeignKey` (`artista` y `festival`), sino que guarda información propia de cada participación:

- `fecha_hora`: cuándo actúa el artista.
- `duracion`: cuánto dura la actuación.
- `cache_pactado`: lo que cobra en ese festival concreto.
- `cancelada`: si la actuación se ha cancelado.

Estos datos no pertenecen ni al artista ni al festival por separado, sino a la combinación de ambos. `Actuacion` tiene además una `ForeignKey` a `Escenario`, que es la cuarta relación ManyToOne y es independiente de la ManyToMany.

### Resumen

| Requisito | Mínimo | Cumplido | Dónde |
|---|---|---|---|
| OneToOne | 3 | 3 | `Festival`, `PerfilArtista`, `CarnetAsistente` |
| ManyToOne | 3 | 4 | `Escenario`, `Entrada` (x2), `Actuacion` |
| ManyToMany | 3 | 3 | `Artista`, `Festival`, `Asistente` |
| ManyToMany con tabla intermedia y atributos extra | 1 | 1 | `Actuacion` |

---

## 6. Tipos de campo usados

Se usan **12 tipos distintos** (el mínimo era 10), sin contar los campos de relación.

| Tipo | Qué guarda | Usado en |
|---|---|---|
| `CharField` | Texto corto con longitud máxima. | `Recinto.nombre`, `Patrocinador.cif`... |
| `TextField` | Texto largo sin límite. | `Festival.descripcion`, `Artista.biografia` |
| `DateField` | Una fecha. | `Festival.fecha_inicio`, `Asistente.fecha_nacimiento` |
| `DateTimeField` | Fecha y hora. | `Actuacion.fecha_hora`, `Entrada.fecha_compra` |
| `BooleanField` | Verdadero o falso. | `Festival.activo`, `Escenario.techado` |
| `PositiveIntegerField` | Entero mayor o igual a 0. | `Recinto.capacidad`, `Festival.aforo` |
| `DecimalField` | Número decimal exacto (dinero). | `Entrada.precio`, `Patrocinador.aportacion` |
| `EmailField` | Texto que valida el formato de email. | `Artista.email`, `Asistente.email` |
| `URLField` | Texto que valida el formato de URL. | `Patrocinador.web`, `PerfilArtista.web` |
| `UUIDField` | Identificador único universal de 128 bits. | `CarnetAsistente.codigo` |
| `DurationField` | Una duración (`timedelta`). | `Actuacion.duracion` |
| `FloatField` | Número con decimales (coma flotante). | `Recinto.latitud`, `Recinto.longitud` |

---

## 7. Parámetros usados

Se usan **13 parámetros distintos** en los campos (el mínimo era 10).

| Parámetro | Qué hace | Ejemplo |
|---|---|---|
| `max_length` | Longitud máxima del texto. | `CharField(max_length=100)` |
| `unique` | No permite valores repetidos en esa columna. | `Patrocinador.cif` |
| `null` | Permite `NULL` en la base de datos. | `Recinto.latitud` |
| `blank` | Permite dejar el campo vacío en formularios. | `Festival.descripcion` |
| `default` | Valor por defecto si no se indica otro. | `Festival.aforo` (1000) |
| `choices` | Lista de pares `(valor_guardado, texto_visible)` que limita las opciones. | `Artista.genero` |
| `help_text` | Texto de ayuda que se muestra en formularios y admin. | `Actuacion.duracion` |
| `verbose_name` | Nombre legible del campo en el admin. | `Recinto.nombre` |
| `validators` | Lista de reglas que debe cumplir el valor. | `MinValueValidator(1)` |
| `max_digits` | Total de dígitos de un `DecimalField`. | `Entrada.precio` (8) |
| `decimal_places` | Cuántos de esos dígitos son decimales. | `Entrada.precio` (2) |
| `auto_now_add` | Rellena la fecha y hora actual solo al crear el registro. | `Entrada.fecha_compra` |
| `editable` | Si es `False`, el campo no aparece en formularios ni se modifica a mano. | `CarnetAsistente.codigo` |

Parámetros de relaciones:

| Parámetro | Qué hace |
|---|---|
| `on_delete=CASCADE` | Si se borra el objeto relacionado, también se borra este. |
| `on_delete=SET_NULL` | Si se borra el objeto relacionado, este campo pasa a `NULL` (requiere `null=True`). |
| `related_name` | Nombre para acceder a la relación en sentido inverso (por ejemplo `recinto.festival`). |
| `through` | Indica la tabla intermedia propia que gestiona una ManyToMany. |

---

## 8. Esquema entidad-relación

![Esquema entidad-relación](docs/esquema_er.png)

- Las tablas `Festival_Patrocinador` y `Asistente_Artista` las crea Django automáticamente para las ManyToMany sin `through`. En el esquema aparecen dibujadas explícitamente para que se vean.
- `Actuacion` es la tabla intermedia manual (`through`) con atributos extra.
- El esquema se ha hecho con [dbdiagram.io](https://dbdiagram.io).

---

## 9. Seeders

Los seeders rellenan la base de datos con **datos fijos y conocidos**. Se ejecutan con:

```bash
python3 manage.py seeders
```

Crean 2 recintos, 2 patrocinadores, 2 festivales, 3 artistas con sus perfiles, 3 escenarios, 3 actuaciones, 2 asistentes con sus carnets y 3 entradas. Se pueden ejecutar varias veces sin duplicar datos.

Archivo: `gestion/management/commands/seeders.py`.

---

## 10. Comando con Faker

Genera 10 registros aleatorios de cada uno de los 10 modelos:

```bash
python3 manage.py poblar
python3 manage.py poblar --cantidad 5
```

Archivo: `gestion/management/commands/poblar.py`.

El comando respeta el orden de dependencias: primero `Recinto` y `Patrocinador`, después `Festival`, `Artista`, `PerfilArtista`, `Escenario`, `Actuacion`, `Asistente`, `CarnetAsistente` y por último `Entrada`.

---

## 11. Backup y fixtures

Hay dos fixtures en `gestion/fixtures/`:

| Archivo | Para qué sirve |
|---|---|
| `backup.json` | Copia de seguridad de los datos de la app `gestion` (rama `Backups`). |
| `datos_pruebas.json` | Datos para probar las URLs. Incluye actuaciones sin escenario, para que la URL 9 muestre resultados. |

Crear un fixture:

```bash
python3 manage.py dumpdata gestion --indent 2 --output gestion/fixtures/backup.json
```

Restaurarlo (con las migraciones ya aplicadas y la base de datos vacía):

```bash
python3 manage.py migrate
python3 manage.py loaddata gestion/fixtures/datos_pruebas.json
```

---

## 12. Código no visto en clase (modelos, comandos y fixtures)

### Comandos propios y seeders

| Elemento | Explicación |
|---|---|
| `management/commands/` | Carpeta donde Django busca comandos propios. El nombre del archivo (`seeders.py`, `poblar.py`) es el nombre del comando. |
| `__init__.py` | Archivo vacío que convierte una carpeta en paquete de Python. Sin él, Django no encuentra el comando. |
| `BaseCommand` | Clase base de la que heredan todos los comandos de Django. |
| `help` | Atributo de la clase `Command`. Texto que se muestra con `python3 manage.py help seeders`. |
| `handle(self, *args, **options)` | Método que se ejecuta al lanzar el comando. |
| `get_or_create(campo=valor, defaults={...})` | Busca un registro con esos campos. Si no existe, lo crea usando también `defaults`. Devuelve una tupla `(objeto, creado)`. Evita duplicados al repetir el seeder. |
| `_` en `recinto, _ = ...` | Nombre convencional para ignorar el segundo valor de la tupla (`creado`). |
| `.add(...)` | Añade objetos a una relación ManyToMany. |
| `timedelta` | Representa una duración o diferencia de tiempo (módulo `datetime`). |
| `date.today()` | Devuelve la fecha de hoy. |
| `timezone.now()` | Fecha y hora actuales teniendo en cuenta la zona horaria de Django. |
| `self.stdout.write(...)` | Escribe un mensaje en la terminal. |
| `self.style.SUCCESS(...)` | Da color verde al mensaje. |

### Modelos

| Elemento | Explicación |
|---|---|
| `uuid.uuid4` | Función que genera un UUID aleatorio. Se pasa **sin paréntesis** para que se ejecute en cada registro nuevo. |
| `MinValueValidator` | Validador de Django que impide valores menores a un mínimo. |
| `class Meta` | Clase interna con configuración extra del modelo. |
| `verbose_name_plural` | Plural que se muestra en el admin (si no, saldría "Actuacions"). |
| `__str__` | Método que define cómo se muestra un objeto como texto. |
| `ManyToManyField` sin `through` | Django crea automáticamente la tabla intermedia. |

### Faker y datos aleatorios

| Elemento | Explicación |
|---|---|
| `Faker("es_ES")` | Crea un generador de datos falsos. `"es_ES"` hace que los nombres, direcciones y teléfonos sean españoles. |
| `fake.unique` | Garantiza que Faker no repita un valor dentro de la misma ejecución. Se usa en campos `unique` como `email`. |
| `fake.numerify('###')` | Sustituye cada `#` por un dígito aleatorio. |
| `fake.bothify('?########')` | Sustituye `?` por una letra y `#` por un dígito. El parámetro `letters` limita qué letras usa. |
| `fake.date_between(start_date, end_date)` | Fecha aleatoria entre dos límites. Admite textos como `"+10d"` (dentro de 10 días) o `"-30y"` (hace 30 años). |
| `fake.date_time_between(..., tzinfo=zona)` | Fecha y hora aleatorias. `tzinfo` evita el aviso de fechas sin zona horaria. |
| `timezone.get_current_timezone()` | Devuelve la zona horaria configurada en Django. |
| `fake.date_of_birth(minimum_age, maximum_age)` | Fecha de nacimiento aleatoria dentro de un rango de edades. |
| `add_arguments(self, parser)` | Método donde se declaran los parámetros opcionales del comando. |
| `parser.add_argument("--cantidad", type=int, default=10)` | Define el parámetro `--cantidad`: de tipo entero y con valor por defecto 10. |
| `options["cantidad"]` | Recoge dentro de `handle` el valor del parámetro. |
| `random.randint(a, b)` | Número entero aleatorio entre `a` y `b`, ambos incluidos. |
| `random.choice(lista)` | Elige un elemento al azar de la lista. |
| `random.sample(lista, k)` | Elige `k` elementos distintos de la lista. |
| `Modelo.objects.create(...)` | Crea y guarda un registro en una sola instrucción. |
| `.set([...])` | Sustituye todos los elementos de una relación ManyToMany por los indicados. |
| `.replace("\n", ", ")` | Cambia los saltos de línea de la dirección por comas. |
| `[g[0] for g in Artista.GENEROS]` | Lista por comprensión: extrae el valor guardado de cada par de `choices`. |

### Fixtures y backup

| Elemento | Explicación |
|---|---|
| fixture | Archivo con una copia de datos de la base de datos (aquí en JSON). |
| `dumpdata gestion` | Vuelca a texto los datos de la app `gestion`. |
| `--indent 2` | Formatea el JSON con sangría de 2 espacios para que sea legible. |
| `--output archivo` | Guarda el resultado en un archivo en vez de mostrarlo en pantalla. |
| `loaddata archivo` | Carga en la base de datos los datos de un fixture. Falla por claves duplicadas si ya existen. |
| `rm db.sqlite3` | Borra la base de datos local para recrearla desde cero (se puede porque no se sube a git). |

---

## 13. URLs y vistas

Todas las vistas están en `gestion/views.py`, las URLs en `gestion/urls.py` y las plantillas en `gestion/templates/gestion/`. Cada vista lleva un comentario que explica qué hace y, en cada QuerySet, el SQL equivalente comentado.

| # | URL | Vista | Plantilla |
|---|---|---|---|
| 1 | `/` | `index` | `index.html` |
| 2 | `/festivales/` | `lista_festivales` | `lista_festivales.html` |
| 3 | `/festival/<int:id>/` | `detalle_festival` | `detalle_festival.html` |
| 4 | `/artistas/<str:genero>/` | `artistas_por_genero` | `artistas_por_genero.html` |
| 5 | `/festival/<int:id>/entradas/<str:tipo>/` | `entradas_festival` | `entradas_festival.html` |
| 6 | `/festivales/anio/<año>/` | `festivales_por_anio` | `festivales_por_anio.html` |
| 7 | `/artistas/top/` | `top_artistas` | `top_artistas.html` |
| 8 | `/estadisticas/entradas/` | `estadisticas_entradas` | `estadisticas_entradas.html` |
| 9 | `/actuaciones/sin-escenario/` | `actuaciones_sin_escenario` | `actuaciones_sin_escenario.html` |
| 10 | `/asistentes/` | `lista_asistentes` | `lista_asistentes.html` |

Todas las plantillas heredan de `base.html` con `{% extends %}`. El index (`/`) enlaza las 10 URLs.

### URL 1: `/` (`index`)

Menú principal con enlaces a todas las URLs del proyecto, con ejemplos que siempre devuelven resultados.

### URL 2: `/festivales/` (`lista_festivales`)

Lista todos los festivales ordenados por fecha de inicio con todos sus datos relacionados.

- **OneToOne**: recinto (`select_related('recinto')`).
- **ManyToMany**: patrocinadores (`prefetch_related('patrocinadores')`).
- **Relación reversa**: escenarios (`prefetch_related('escenarios')`).
- **`order_by`**: `fecha_inicio`.
- **Optimización**: 3 consultas SQL fijas.

### URL 3: `/festival/<int:id>/` (`detalle_festival`)

Muestra un festival concreto con toda su información relacionada.

- **Parámetro entero**: `<int:id>`.
- **OneToOne**: recinto.
- **ManyToMany**: patrocinadores.
- **ManyToMany con tabla intermedia**: artistas a través de `Actuacion`, con fecha, duración, caché y si está cancelada.
- **ManyToOne**: escenarios y entradas, estas con su asistente.
- **Error 404** si el festival no existe (`get_object_or_404`).
- **Optimización**: 5 consultas SQL fijas.

### URL 4: `/artistas/<str:genero>/` (`artistas_por_genero`)

Lista los artistas de un género con popularidad de 40 o más, de más a menos populares.

- **Parámetro str**: `<str:genero>`.
- **Filtro con AND**: `filter(genero=genero, popularidad__gte=40)`.
- **OneToOne**: perfil (`select_related('perfil')`).
- **ManyToMany con tabla intermedia**: actuaciones con festival y escenario (`Prefetch` sobre `actuacion_set`).
- **ManyToMany reversa**: seguidores (`prefetch_related('seguidores')`).
- **`order_by`**: `-popularidad`.
- **Error 404** si el género no existe.
- **Optimización**: 3 consultas SQL fijas.

### URL 5: `/festival/<int:id>/entradas/<str:tipo>/` (`entradas_festival`)

Lista las entradas de un tipo (general, vip o abono) vendidas para un festival, de más a menos caras.

- **Dos parámetros**: `<int:id>` y `<str:tipo>`.
- **Filtro con AND**: `filter(festival=festival, tipo=tipo)`.
- **ManyToOne**: entrada con su asistente.
- **OneToOne reversa**: carnet (`select_related('asistente__carnet')`).
- **ManyToMany**: artistas favoritos (`prefetch_related('asistente__artistas_favoritos')`).
- **`order_by`**: `-precio`.
- **Error 404** si el festival o el tipo no existen.
- **Optimización**: 3 consultas SQL fijas.

### URL 6: `/festivales/anio/<año>/` (`festivales_por_anio`)

Lista los festivales que empiezan o terminan en el año indicado.

- **`re_path`**: `r'^festivales/anio/(?P<anio>[0-9]{4})/$'`, solo admite años de 4 dígitos.
- **Filtro con OR**: `filter(Q(fecha_inicio__year=anio) | Q(fecha_fin__year=anio))`.
- **OneToOne**: recinto.
- **ManyToMany**: patrocinadores.
- **ManyToOne reversa**: escenarios.
- **ManyToMany con tabla intermedia**: actuaciones con artista y escenario.
- **`order_by`**: `fecha_inicio`.
- **Optimización**: 4 consultas SQL fijas.

### URL 7: `/artistas/top/` (`top_artistas`)

Muestra los 5 artistas más populares.

- **`order_by`**: `order_by('-popularidad', 'nombre_artistico')`.
- **Límite**: `[:5]`, equivalente a `LIMIT 5`.
- **OneToOne**: perfil.
- **ManyToMany con tabla intermedia**: actuaciones con festival y escenario.
- **ManyToMany reversa**: seguidores.
- **Optimización**: 3 consultas SQL fijas.
- Está declarada antes que `artistas/<str:genero>/` para que `top` no se interprete como un género.

### URL 8: `/estadisticas/entradas/` (`estadisticas_entradas`)

Muestra estadísticas globales de las entradas vendidas y las 5 más caras.

- **`aggregate`**: `Count`, `Sum`, `Avg`, `Max` y `Min`, incluyendo un agregado condicional (`Count('id', filter=Q(usada=True))`).
- **ManyToOne**: entrada con su asistente y su festival.
- **OneToOne**: carnet (`asistente__carnet`) y recinto (`festival__recinto`).
- **`order_by`** y **límite**: `order_by('-precio')[:5]`.
- **Optimización**: 2 consultas SQL.

Investigación sobre `aggregate`: calcula un valor a partir de todas las filas de un QuerySet y devuelve un diccionario. Es una operación final: se ejecuta en el momento y no admite más filtros encadenados. Se diferencia de `annotate`, que añade el cálculo a cada objeto en lugar de devolver un único resultado.

### URL 9: `/actuaciones/sin-escenario/` (`actuaciones_sin_escenario`)

Lista las actuaciones que todavía no tienen escenario asignado.

- **Filtro con `None` en una tabla intermedia**: `filter(escenario__isnull=True)` sobre `Actuacion`.
- **OneToOne**: perfil del artista y recinto del festival.
- **ManyToOne**: festival de la actuación.
- **ManyToMany**: seguidores del artista (`artista__seguidores`).
- **Relación reversa**: escenarios disponibles del festival (`festival__escenarios`).
- **`order_by`**: `fecha_hora`.
- **Optimización**: 3 consultas SQL fijas.
- El fixture de pruebas incluye actuaciones sin escenario para que la URL muestre resultados.

### URL 10: `/asistentes/` (`lista_asistentes`)

Lista todos los asistentes con su carnet, sus artistas favoritos y sus entradas.

- **OneToOne**: carnet (`select_related('carnet')`).
- **ManyToMany**: artistas favoritos.
- **ManyToOne reversa**: entradas con su festival (`Prefetch` sobre `entradas`).
- **`order_by`**: `order_by('apellidos', 'nombre')`.
- **Optimización**: 3 consultas SQL fijas.

### Resumen de requisitos de la tarea

| Requisito | Dónde se cumple |
|---|---|
| 10 URLs con vistas, QuerySet y plantillas | Tabla de la sección 13 |
| Una rama por URL fusionada en `Vistas` | Ramas `url_*` (sección 2) |
| Datos entre tablas ManyToMany, OneToOne y ManyToOne | URL 2 a 10 |
| Comentario en cada vista | Todas |
| SQL equivalente comentado en cada QuerySet | Todas |
| 4 páginas de error personalizadas | Sección 14 |
| Muestra toda la información de los modelos relacionados | Todas las plantillas |
| Queries optimizadas | `select_related`, `prefetch_related` y `Prefetch` |
| `re_path` | URL 6 |
| Dos parámetros | URL 5 |
| Parámetro entero | URL 3 y 5 |
| Parámetro str | URL 4 y 5 |
| Filtro AND | URL 4 y 5 |
| Filtro OR | URL 6 |
| `aggregate` | URL 8 |
| Relación reversa | URL 2, 6, 9 y 10 |
| `order_by` | Todas |
| Límite | URL 7 y 8 |
| Filtro con `None` en tabla intermedia | URL 9 |
| Index con acceso a todas las URLs | URL 1 |
| Fixture de pruebas | `gestion/fixtures/datos_pruebas.json` |
| Modo producción | Sección 14 |

---

## 14. Páginas de error y modo producción

### Páginas de error personalizadas

| Error | Vista | Plantilla | Cuándo ocurre |
|---|---|---|---|
| 400 | `error_400` | `errores/400.html` | Petición incorrecta |
| 403 | `error_403` | `errores/403.html` | Acceso prohibido |
| 404 | `error_404` | `errores/404.html` | Página o recurso no encontrado |
| 500 | `error_500` | `errores/500.html` | Error interno del servidor |

Se registran en `festivales/urls.py` con `handler400`, `handler403`, `handler404` y `handler500`. La plantilla del error 500 es independiente de `base.html` para que no falle si el problema está en la plantilla base.

### Modo producción

En `festivales/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

Con `DEBUG = False` Django muestra las páginas de error personalizadas en lugar de las técnicas de depuración. El proyecto no depende de archivos estáticos (el CSS está dentro de `base.html`). Para ver el panel `/admin/` con estilos en pruebas:

```bash
python3 manage.py runserver --insecure
```

---

## 15. Cómo probar el proyecto

```bash
git clone <URL-del-repositorio>
cd festivales-django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py loaddata gestion/fixtures/datos_pruebas.json
python3 manage.py runserver
```

Abrir `http://127.0.0.1:8000/`. El index enlaza las 10 URLs.

El fixture `datos_pruebas.json` contiene datos de todos los modelos y varias actuaciones sin escenario, para que la URL 9 muestre resultados. Debe cargarse en una base de datos vacía (recién migrada). Si ya hay datos, borrar `db.sqlite3` y repetir `migrate`.

---

## 16. Código no visto en clase (URLs y vistas)

| Elemento | Explicación |
|---|---|
| `include('gestion.urls')` | Incluye las URLs de la app dentro de las del proyecto. |
| `path('', vista, name='x')` | Asocia una URL a una vista. `name` permite usarla con `{% url 'x' %}`. |
| `{% extends %}` y `{% block %}` | Herencia de plantillas: `base.html` define la estructura y cada página rellena sus bloques. |
| `{% url 'nombre' valor %}` | Genera la URL a partir de su `name`, pasando los parámetros en orden. |
| `{% for %} ... {% empty %}` | Bucle de plantilla. El bloque `empty` se muestra si no hay elementos. |
| `forloop.counter` | Contador del bucle, empieza en 1. |
| `get_<campo>_display` | Método que Django crea para campos con `choices`: devuelve el texto legible. |
| `\|date:"d/m/Y"` | Filtro que da formato a una fecha. |
| `\|default:0` | Muestra el valor indicado si el original es vacío o `None`. |
| `\|floatformat:2` | Redondea un número a 2 decimales. |
| `select_related('campo')` | Trae el objeto relacionado en la misma consulta con un `JOIN`. Para OneToOne y ForeignKey. |
| `prefetch_related('campo')` | Hace una consulta aparte para ManyToMany o relaciones reversas y las une en Python. |
| `Prefetch('rel', queryset=...)` | `prefetch_related` con una consulta propia, para optimizar lo que se trae. |
| `actuacion_set` | Nombre automático de la relación inversa de una `ForeignKey` sin `related_name`. |
| `'a__b'` | El doble guion bajo recorre relaciones encadenadas o aplica un filtro (`popularidad__gte`). |
| `__gte`, `__year`, `__isnull` | Filtros: mayor o igual, año de una fecha, es `NULL`. |
| `filter(a=1, b=2)` | Varias condiciones en un mismo `filter` se combinan con `AND`. |
| `Q(a) \| Q(b)` | Une condiciones con `OR`. `&` es AND y `~Q()` es NOT. |
| `'-campo'` en `order_by` | Orden descendente. Se pueden indicar varios campos. |
| `queryset[:5]` | Límite de resultados, equivale a `LIMIT 5`. Va después de `order_by` y `filter`. |
| `aggregate(x=Funcion('campo'))` | Calcula un valor sobre todas las filas y devuelve un diccionario. |
| `Count`, `Sum`, `Avg`, `Max`, `Min` | Funciones de agregación (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`). |
| `Count('id', filter=Q(...))` | Agregado condicional: cuenta solo las filas que cumplen la condición. |
| `get_object_or_404` | Busca un objeto y, si no existe, devuelve un 404. |
| `raise Http404(...)` | Lanza un error 404 manualmente. |
| `<int:id>` y `<str:genero>` | Convertidores de URL: capturan un entero o un texto y lo pasan a la vista. |
| `re_path(r'...', vista)` | URL con expresión regular. `(?P<anio>[0-9]{4})` es un grupo con nombre de 4 dígitos. |
| `dict(Artista.GENEROS)` | Convierte la lista de `choices` en un diccionario `{valor: texto}`. |
| `handler404 = 'gestion.views.error_404'` | Indica qué vista usa Django para ese error. Existen 400, 403, 404 y 500. |
| `render(..., status=404)` | Fija el código HTTP de la respuesta. |
| `DEBUG = False` y `ALLOWED_HOSTS` | Modo producción: oculta los errores técnicos y limita las direcciones permitidas. |
| `runserver --insecure` | Sirve estáticos con `DEBUG = False`. Solo para pruebas. |
| `.update(campo=valor)` | Modifica en una sola consulta todas las filas de un QuerySet. |