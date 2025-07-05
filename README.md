# Adoptab

## Descripción

Un proyecto para que los grupos de rescate o individuales, puedan dar una muestra de los animales rescatados para que las personas puedan verlos, y aquellos que estén interesados puedan ver la información de las mascotas que actualmente estén en posibilidad de ser adoptadas.

## Instalación

### 1. Clonar Repositorio

```python
# Crear carpeta(Opcional)
mkdir adoptab
cd adoptab

# Clonar git
git clone https://github.com/NoMeLlamoDante/adoptab.git
cd adoptab
```

### 2. Entorno Virtual

```python
# Crear entorno virtual
python3 -m venv env

# Ejecutar entorno virtual
source env/bin/activate

#Instalar requerimientos
pip install -r requirements.txt
```

### 3. Archivos de configración

Existen 2 archivos en los cuales se encuentran los datos de configuración necesarios para ejecutar el programa, ambos archivos se pueden configurar mediante un solo comando ejecuntando, el cual los cambiará a su configuración por defecto.

```python
# archivo .env
mv example.env .env
# archivo my.cnf
mv adoptab/example.my.cnf adoptab/my.cnf

# Alternativa
make init
```

#### 3.1 .env

En este archivo se encuentran las configuraciones asosiadas al space dentro de digital ocean (equivalente a bucket de AWS), así como las variables de entorno utilizadas en django settings y se encuentra en la raiz.

```Shell
#### Digital ocean info
DO_ACCESS_KEY='ACCESS_KEY'
DO_SECRET_KEY='PRIVATE_KEY'

DO_SPACES_SPACE_NAME='BUCKET_NAMESPACE'
DO_SPACES_ENDPOINT_URL='https://BUCKET_NAMESPACE.REGION.digitaloceanspaces.com'
DO_REGION='REGION'

DEBUG=True
ALLOWED=['*']

SECRET_KEY = 'SECRET_KEY_DJANGO'
```

### 3.2 my.conf

En este archivo se encuentran los datos para conectarse a la base de datos de MySQL, se encuentra dentro de la carpeta nucleo de la aplicación

```Shell
# my.cnf
[client]
database = database_name
user = user_database
password = 'password'
default-character-set = utf8
```

### 3. Base de datos

Posteriormente a la configuración de los archivos de entorno, se hace la adecuación de la base de datos, mediante el comando de django para aello

```python
# Crear migraciones
python3 manage.py makekmigrations
# ejecutar migraciones
python3 manage.py migrate

# Alternativa
make mg
```

## Ejecutar localmente

### 1. Crear Super usuario

```python
python3 manage.py createsuperusaer

# Alternativa
make csu
```

### 2. Ejecutar

```python
python3 manage.py runserver

# Alternativa
make run

```

## Roadmap

-   Agregar previas de las mascotas a la pantalla principal
-   filtrar las mascotas cargadas por cada usuario
-   mostrar info para contacto de adopción (De manera segura)
-   cambiar estado de las mascotas (en adopción, adoptadas)
-   filtrar solo por mascotas en adopción
-   agregar información de las adopciones
    -   costo o cuota de recuperación (si es que tiene)
    -   Vacunas o tratamientos
