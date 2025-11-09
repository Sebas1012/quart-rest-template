# Quart REST API Template

Una plantilla profesional y moderna para crear APIs REST asincrónicas usando **Quart**, el framework web asincrónico para Python. Esta plantilla incluye configuración completa, autenticación JWT, validación de datos, y ejemplos de rutas.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso](#uso)
- [Autenticación JWT](#autenticación-jwt)
- [Base de Datos](#base-de-datos)
- [Documentación API](#documentación-api)
- [Desarrollo](#desarrollo)
- [Contribución](#contribución)

---

## ✨ Características

- ⚡ **Asincrónico**: Basado en Quart para máximo rendimiento con async/await
- 🔐 **Autenticación JWT**: Sistema completo de autenticación con JWT integrado
- 📚 **Documentación Automática**: Generación automática de documentación con Quart-Schema
- 🗄️ **ORM Asincrónico**: Tortoise ORM para operaciones de base de datos async
- ✅ **Validación de Datos**: Integración con Pydantic para validación robusta
- 🔒 **Control de Roles**: Sistema de validación de roles para proteger rutas
- 🛠️ **Configuración Flexible**: Manejo de configuración con variables de entorno
- 📦 **Gestión de Dependencias**: Poetry para un manejo reproducible de dependencias

---

## 📦 Requisitos

- Python 3.12 o superior
- Poetry (gestor de dependencias)
- PostgreSQL o base de datos compatible (opcional, configurable)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Sebas1012/quart-rest-template.git
cd quart-rest-template
```

### 2. Instalar dependencias

```bash
poetry install
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración de Base de Datos
DB_URI=postgres://usuario:contraseña@localhost:5432/nombre_bd

# Configuración JWT
JWT_KEY=tu_clave_secreta_aqui_cambiar_en_produccion

# Configuración de la aplicación
DEBUG=True
HOST=0.0.0.0
PORT=5000
```

### 4. Ejecutar la aplicación

```bash
poetry run quart --app app:create_app --debug run
```

La API estará disponible en `http://localhost:5000`

---

## ⚙️ Configuración

### Variables de Entorno

El archivo `app/config.py` gestiona la configuración de la aplicación:

```python
TORTOISE_DATABASE_URI       # URI de conexión a la base de datos
JWT_ACCESS_TOKEN_EXPIRES    # Tiempo de expiración del token (defecto: 30 min)
SESSION_REFRESH_EACH_REQUEST # Renovar sesión en cada solicitud
JWT_SECRET_KEY              # Clave secreta para firmar JWT
```

### Personalización

Edita `app/config.py` para ajustar la configuración según tus necesidades.

---

## 📁 Estructura del Proyecto

```
quart-rest-template/
├── main.py                    # Punto de entrada de la aplicación
├── pyproject.toml             # Configuración y dependencias de Poetry
├── README.md                  # Este archivo
├── .env                       # Variables de entorno (no versionado)
├── .gitignore                 # Archivos ignorados por git
│
└── app/
    ├── __init__.py            # Factory function create_app()
    ├── config.py              # Configuración de la aplicación
    │
    ├── models/
    │   ├── __init__.py
    │   └── auth.py            # Modelos de autenticación (User)
    │
    ├── routes/
    │   ├── __init__.py
    │   ├── hello.py           # Rutas de prueba
    │   └── auth.py            # Rutas de autenticación (login, registro)
    │
    └── utils/
        ├── __init__.py
        ├── db.py              # Inicialización y gestión de BD
        ├── docs.py            # Configuración de documentación
        ├── jwt.py             # Configuración de JWT
        └── role_validator.py  # Validadores de roles y permisos
```

---

## 🔧 Uso

### Ejecutar el servidor

```bash
# Modo desarrollo con hot-reload
poetry run quart --app app:create_app --debug run

# Modo producción
poetry run quart --app app:create_app run
```

### Instalar nuevas dependencias

```bash
poetry add nombre_del_paquete
```

### Ejecutar comandos con Poetry

```bash
poetry run python script.py
poetry run pytest
```

---

## 🔐 Autenticación JWT

### Crear Usuario

```bash
curl -X POST http://localhost:5000/api/v1/auth/create-user \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "contraseña123"
  }'
```

**Respuesta Exitosa (201):**
```json
{
  "message": "User created successfully"
}
```

**Error - Usuario existe (409):**
```json
{
  "message": "User already exists"
}
```

### Obtener Token

```bash
curl -X POST http://localhost:5000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "contraseña123"
  }'
```

**Respuesta Exitosa (200):**
```json
{
  "user_id": 1,
  "user_role": "Pending",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Error - Credenciales inválidas (401):**
```json
{
  "message": "Invalid username or password"
}
```

### Usar el Token

Incluye el token en el header `Authorization` de tus solicitudes:

```bash
curl -X GET http://localhost:5000/api/v1/hello \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### Obtener el Endpoint Hello

Para probar que la API funciona:

```bash
curl -X GET http://localhost:5000/api/v1/hello
```

**Respuesta:**
```json
{
  "message": "Hello, World!"
}
```

---

## 🗄️ Base de Datos

Este template usa **Tortoise ORM** para operaciones de base de datos asincrónicas con **PostgreSQL**.

### Configurar Base de Datos

En `.env`, configura la URI de conexión a PostgreSQL:

```env
DB_URI=postgres://usuario:contraseña@localhost:5432/nombre_bd
```

**Asegúrate de que PostgreSQL está instalado y ejecutándose** antes de iniciar la aplicación.

### Modelos Existentes

El proyecto incluye un modelo `UserLogin` en `app/models/auth.py`:

```python
from tortoise import Model, fields

class UserLogin(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255)
    create_at = fields.DatetimeField(auto_now_add=True)
    user_rol = fields.CharField(max_length=30, default="Pending")

    def verify_password(self, raw_password: str) -> bool:
        return pbkdf2_sha256.verify(raw_password, self.password)
```

### Crear Nuevos Modelos

En `app/models/`, crea archivos con tus modelos:

```python
from tortoise import Model, fields

class Producto(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=100)
    precio = fields.DecimalField(max_digits=10, decimal_places=2)
    creado_en = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "productos"
```

---

## 📚 Documentación API

La documentación se genera automáticamente usando **Quart-Schema**.

Accede a la documentación interactiva en:
- **Swagger UI**: `http://localhost:5000/docs`
- **ReDoc**: `http://localhost:5000/redocs`
- **JSON Schema**: `http://localhost:5000/openapi.json`

### Documentar Rutas

Usa decoradores de Quart-Schema y docstrings para documentar tus endpoints:

```python
from quart import Blueprint
from quart_schema import validate_request, validate_response
from pydantic import BaseModel

bp = Blueprint('productos', __name__, url_prefix='/api/v1/productos')

class ProductoRequest(BaseModel):
    nombre: str
    precio: float

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float

@bp.route('/', methods=['POST'])
@validate_request(ProductoRequest)
@validate_response(ProductoResponse, 201)
async def crear_producto(data: ProductoRequest):
    """Crear un nuevo producto"""
    # Lógica para crear producto
    return {'id': 1, 'nombre': data.nombre, 'precio': data.precio}, 201
```

---

## 🛠️ Desarrollo

### Instalar herramientas de desarrollo

```bash
poetry install
```

### Formatear código

```bash
poetry run black app/ main.py
```

### Ejecutar tests (si existen)

```bash
poetry run pytest
```

### Estructura de archivos para desarrollo

Cuando agregues nuevas rutas:

1. Crea un nuevo archivo en `app/routes/`
2. Define el blueprint con `url_prefix='/api/v1/<recurso>'`
3. Registra el blueprint en `app/__init__.py`

Ejemplo:

```python
# app/routes/productos.py
from quart import Blueprint
from quart_schema import validate_request, validate_response
from pydantic import BaseModel

bp = Blueprint('productos', __name__, url_prefix='/api/v1/productos')

class ProductoRequest(BaseModel):
    nombre: str
    precio: float

@bp.route('/', methods=['POST'])
@validate_request(ProductoRequest)
async def crear_producto(data: ProductoRequest):
    return {'message': 'Producto creado'}, 201

# En app/__init__.py
from .routes.productos import bp as productos_bp
app.register_blueprint(productos_bp)
```

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📞 Soporte

Para reportar bugs o sugerir mejoras, abre un issue en el repositorio.

---

## 🔗 Enlaces Útiles

- [Documentación de Quart](https://quart.palletsprojects.com/)
- [Documentación de Tortoise ORM](https://tortoise.readthedocs.io/)
- [Documentación de Pydantic](https://docs.pydantic.dev/)
- [JWT Extended](https://flask-jwt-extended.readthedocs.io/)

---

**Creado por:** Sebastian Henao
**Última actualización:** Noviembre 2025 