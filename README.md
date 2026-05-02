# FitStore - E-commerce de Prendas Deportivas

## 📋 Descripción General

**FitStore** es una aplicación de comercio electrónico especializada en la venta de prendas deportivas. Está construida con una arquitectura moderna basada en **FastAPI** para el backend, **SQLModel** para la gestión de datos, y **HTML/CSS/JavaScript** para el frontend.

El proyecto implementa un sistema completo de e-commerce con autenticación de usuarios, gestión de categorías y productos, carrito de compras, y control de acceso basado en roles (clientes y administradores).

---

## ✨ Características Principales

### Para Clientes
- ✅ Registro e inicio de sesión seguro con tokens JWT
- ✅ Visualizar catálogo completo de productos
- ✅ Filtrar productos por categoría
- ✅ Ver detalles de productos (nombre, precio, descripción, stock)
- ✅ Agregar productos al carrito de compras
- ✅ Gestionar carrito (ver, agregar, eliminar productos)
- ✅ Ver su perfil personal

### Para Administradores
- ✅ Crear, editar y eliminar categorías
- ✅ Crear, editar y eliminar productos
- ✅ Gestionar inventario (actualizar stock)
- ✅ Crear otros usuarios administradores
- ✅ Eliminar usuarios (cuando sea necesario)

### Sistema General
- ✅ Autenticación JWT con tokens de acceso
- ✅ Control de acceso basado en roles (RBAC)
- ✅ Base de datos PostgreSQL relacional
- ✅ API RESTful documentada automáticamente con Swagger UI
- ✅ Validación de datos con Pydantic
- ✅ Manejo de errores robusto

---

## 🛠 Stack Tecnológico

### Backend
| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **FastAPI** | 0.135.3 | Framework web asincrónico |
| **SQLModel** | 0.0.38 | ORM para manejo de base de datos |
| **Pydantic** | 2.12.5 | Validación de datos |
| **python-jose** | 3.5.0 | Generación y verificación de JWT |
| **passlib** | 1.7.4 | Hash seguro de contraseñas |
| **bcrypt** | 3.2.2 | Algoritmo de encriptación |
| **psycopg2** | 2.9.11 | Driver PostgreSQL |

### Base de Datos
| Tecnología | Propósito |
|-----------|----------|
| **PostgreSQL** | Base de datos relacional principal |
| **Docker Compose** | Orquestación de contenedores |

### Frontend
| Tecnología | Propósito |
|-----------|----------|
| **HTML5** | Estructura de la interfaz |
| **CSS3** | Estilos y diseño responsive |
| **JavaScript** | Interactividad e integración con API |

### Herramientas de Desarrollo
- **Python 3.x** - Lenguaje de programación
- **pip** - Gestor de paquetes Python
- **python-dotenv** - Gestión de variables de entorno
- **Uvicorn** - Servidor ASGI

---

## 📁 Estructura del Proyecto

```
e-commerce_FitStore/
├── main.py                      # Punto de entrada principal de la aplicación
├── config.py                    # Configuración (claves secretas, algoritmos)
├── database.py                  # Configuración de conexión a BD
├── requirements.txt             # Dependencias de Python
├── docker-compose.yml           # Configuración de PostgreSQL en Docker
├── .env                         # Variables de entorno (LOCAL - no versionar)
├── .gitignore                   # Archivos a ignorar en Git
│
├── frontend/                    # Interfaz del usuario
│   ├── index.html              # Página principal
│   ├── home.html               # Página de inicio/dashboard
│   ├── productos.html          # Listado de productos
│   ├── admin.html              # Panel de administración
│   ├── app.js                  # Lógica de cliente (llamadas a API)
│   └── styles.css              # Estilos globales
│
├── models/                      # Modelos de datos (SQLModel)
│   ├── __init__.py
│   ├── user.py                 # Modelo Usuario
│   ├── product.py              # Modelo Producto
│   ├── category.py             # Modelo Categoría
│   └── cart.py                 # Modelo Carrito (en memoria)
│
├── schemas/                     # Esquemas Pydantic (validación)
│   ├── __init__.py
│   ├── user.py                 # Esquemas de Usuario
│   ├── product.py              # Esquemas de Producto
│   ├── category.py             # Esquemas de Categoría
│   └── cart.py                 # Esquemas de Carrito
│
├── routes/                      # Rutas/Endpoints de la API
│   ├── user_routes.py          # Endpoints: usuarios, login, admin
│   ├── product_routes.py       # Endpoints: CRUD productos
│   ├── category_routes.py      # Endpoints: CRUD categorías
│   └── cart_routes.py          # Endpoints: carrito de compras
│
└── services/                    # Lógica de negocio y utilidades
    ├── __init__.py
    ├── auth.py                 # Funciones de autenticación (JWT, hashing)
    ├── deps.py                 # Dependencias (verificación de tokens)
    └── utils.py                # Funciones auxiliares
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos
- **Python 3.8+**
- **PostgreSQL 12+** (o Docker instalado)
- **pip** (gestor de paquetes Python)
- **Git** (opcional, para clonar el repositorio)

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Si usas Git
git clone <url-del-repositorio>
cd e-commerce_FitStore

# O descarga el ZIP y extrae
```

### Paso 2: Crear un Entorno Virtual

```bash
# En Linux/Mac
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Configuración de Autenticación
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración de Base de Datos
DATABASE_URL=postgresql://ecommerce_user:161901@localhost:5432/ecommerce_db
```

**⚠️ Nota:** En producción, cambia `SECRET_KEY` a un valor único y seguro.

### Paso 5: Iniciar la Base de Datos con Docker

```bash
# Inicia PostgreSQL en un contenedor
docker-compose up -d

# Verifica que el contenedor esté corriendo
docker ps
```

Si no quieres usar Docker, configura PostgreSQL manualmente en tu sistema.

### Paso 6: Ejecutar la Aplicación

```bash
# Inicia el servidor FastAPI
uvicorn main:app --reload

# El servidor estará disponible en http://localhost:8000
```

### Paso 7: Acceder a la Aplicación

- **Frontend:** http://localhost:8000/static/index.html
- **API Docs (Swagger UI):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc

---

## 📡 Documentación de Endpoints

### 🔐 Autenticación

#### POST `/usuarios/`
**Registrar nuevo usuario (cliente)**

```bash
curl -X POST "http://localhost:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "password": "micontraseña123"
  }'
```

**Respuesta:**
```json
{
  "message": "Usuario conectado correctamente"
}
```

---

#### POST `/usuarios/login`
**Iniciar sesión y obtener token JWT**

```bash
curl -X POST "http://localhost:8000/usuarios/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "micontraseña123"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

#### POST `/usuarios/crear-admin`
**Crear un nuevo usuario administrador (solo admin)**

```bash
curl -X POST "http://localhost:8000/usuarios/crear-admin" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "nombre": "Admin Usuario",
    "email": "admin@example.com",
    "password": "contraseña_admin"
  }'
```

---

#### GET `/usuarios/mi-perfil`
**Obtener datos del usuario actual (autenticado)**

```bash
curl -X GET "http://localhost:8000/usuarios/mi-perfil" \
  -H "Authorization: Bearer <access_token>"
```

**Respuesta:**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "rol": "cliente"
}
```

---

#### DELETE `/usuarios/{usuario_id}`
**Eliminar un usuario (solo admin)**

```bash
curl -X DELETE "http://localhost:8000/usuarios/5" \
  -H "Authorization: Bearer <access_token>"
```

---

### 📦 Categorías

#### GET `/categorias/`
**Obtener todas las categorías**

```bash
curl -X GET "http://localhost:8000/categorias/"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Ropa deportiva",
    "descripcion": "Camisetas, pantalones y accesorios"
  },
  {
    "id": 2,
    "nombre": "Calzado deportivo",
    "descripcion": "Zapatillas y botas deportivas"
  }
]
```

---

#### GET `/categorias/{categoria_id}`
**Obtener una categoría específica**

```bash
curl -X GET "http://localhost:8000/categorias/1"
```

---

#### POST `/categorias/`
**Crear nueva categoría (solo admin)**

```bash
curl -X POST "http://localhost:8000/categorias/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "nombre": "Accesorios deportivos",
    "descripcion": "Mochilas, bandas, cinturones"
  }'
```

---

#### PUT `/categorias/{categoria_id}`
**Actualizar una categoría (solo admin)**

```bash
curl -X PUT "http://localhost:8000/categorias/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "nombre": "Ropa de entrenamiento",
    "descripcion": "Ropa especializada para entrenamientos"
  }'
```

---

#### DELETE `/categorias/{categoria_id}`
**Eliminar una categoría (solo admin)**

```bash
curl -X DELETE "http://localhost:8000/categorias/1" \
  -H "Authorization: Bearer <access_token>"
```

---

### 🏃 Productos

#### GET `/productos/`
**Obtener todos los productos**

```bash
curl -X GET "http://localhost:8000/productos/"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "categoria_id": 1,
    "nombre": "Camiseta deportiva",
    "precio": 29.99,
    "descripcion": "Camiseta transpirable para entrenamientos",
    "stock": 50,
    "imagen": "https://...",
    "created_at": "2026-01-15T10:30:00"
  }
]
```

---

#### GET `/productos/{producto_id}`
**Obtener un producto específico**

```bash
curl -X GET "http://localhost:8000/productos/1"
```

---

#### GET `/productos/categoria/{categoria_id}`
**Obtener productos por categoría**

```bash
curl -X GET "http://localhost:8000/productos/categoria/1"
```

---

#### POST `/productos/`
**Crear nuevo producto (solo admin)**

```bash
curl -X POST "http://localhost:8000/productos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "nombre": "Pantalón deportivo",
    "precio": 49.99,
    "descripcion": "Pantalón cómodo para entrenamientos",
    "stock": 30,
    "categoria_id": 1,
    "imagen": "https://example.com/pantalon.jpg"
  }'
```

---

#### PUT `/productos/{producto_id}`
**Actualizar un producto (solo admin)**

```bash
curl -X PUT "http://localhost:8000/productos/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "precio": 34.99,
    "stock": 45
  }'
```

---

#### DELETE `/productos/{producto_id}`
**Eliminar un producto (solo admin)**

```bash
curl -X DELETE "http://localhost:8000/productos/1" \
  -H "Authorization: Bearer <access_token>"
```

---

### 🛒 Carrito de Compras

#### GET `/carrito/{usuario_id}`
**Obtener carrito de un usuario**

```bash
curl -X GET "http://localhost:8000/carrito/1"
```

**Respuesta:**
```json
[
  {
    "producto_id": 1,
    "cantidad": 2
  },
  {
    "producto_id": 3,
    "cantidad": 1
  }
]
```

---

#### POST `/carrito/{usuario_id}`
**Agregar producto al carrito**

```bash
curl -X POST "http://localhost:8000/carrito/1" \
  -H "Content-Type: application/json" \
  -d '{
    "producto_id": 2,
    "cantidad": 1
  }'
```

---

#### DELETE `/carrito/{usuario_id}?producto_id=2`
**Eliminar producto del carrito**

```bash
curl -X DELETE "http://localhost:8000/carrito/1?producto_id=2"
```

---

## 🗄 Modelos de Datos

### Usuario (Usuario)

```python
class Usuario(SQLModel, table=True):
    id: Optional[int] = Campo principal
    nombre: str              # Nombre completo (máx 100 caracteres)
    email: str              # Email único (máx 150 caracteres)
    password: str           # Contraseña hasheada (máx 255 caracteres)
    rol: str                # "cliente" o "admin"
    created_at: datetime    # Fecha de creación
```

---

### Producto (Producto)

```python
class Producto(SQLModel, table=True):
    id: Optional[int]        # Campo principal
    categoria_id: Optional[int]  # Relación con Categoría
    nombre: str              # Nombre del producto (máx 150 caracteres)
    precio: float            # Precio (debe ser >= 0)
    descripcion: Optional[str]   # Descripción del producto
    stock: int               # Cantidad disponible (debe ser >= 0)
    imagen: Optional[str]    # URL de la imagen (máx 300 caracteres)
    created_at: datetime     # Fecha de creación
```

---

### Categoría (Categoria)

```python
class Categoria(SQLModel, table=True):
    id: Optional[int]        # Campo principal
    nombre: str              # Nombre único (máx 100 caracteres)
    descripcion: Optional[str]   # Descripción de la categoría
```

---

### Carrito (Modelo en Memoria)

```python
# Estructura: {usuario_id: [items]}
carritos = {
    1: [
        {"producto_id": 1, "cantidad": 2},
        {"producto_id": 3, "cantidad": 1}
    ]
}
```

⚠️ **Nota:** El carrito está almacenado en memoria (no persiste en BD). En producción, deberías crear un modelo Carrito en la BD.

---

## 🔐 Autenticación y Autorización

### Flujo de Autenticación JWT

1. **Usuario se registra** → Contraseña se hashea con bcrypt y se almacena
2. **Usuario inicia sesión** → Se verifica email y contraseña
3. **Sistema genera JWT** → Token contiene `usuario_id` y fecha de expiración
4. **Cliente envía JWT** → En header `Authorization: Bearer <token>`
5. **API verifica JWT** → Decodifica token y valida firma

### Función de Hash de Contraseñas

```python
# En services/auth.py
def crear_hash_password(password: str):
    return pwd_context.hash(password)  # Usa bcrypt

def verificar_password(texto_plano, hashed):
    return pwd_context.verify(texto_plano, hashed)
```

### Roles y Permisos

| Acción | Cliente | Admin |
|--------|---------|-------|
| Ver productos | ✅ | ✅ |
| Ver carrito | ✅ | ✅ |
| Agregar al carrito | ✅ | ✅ |
| Crear categoría | ❌ | ✅ |
| Crear producto | ❌ | ✅ |
| Editar producto | ❌ | ✅ |
| Eliminar producto | ❌ | ✅ |
| Eliminar usuario | ❌ | ✅ |
| Crear admin | ❌ | ✅ |

---

## 💻 Frontend - Interfaz de Usuario

### Archivos HTML

#### **index.html**
- Página de login/registro
- Formulario de autenticación
- Redirección según rol

#### **home.html**
- Dashboard principal después del login
- Bienvenida personalizad
- Enlaces a productos y carrito

#### **productos.html**
- Listado completo de productos
- Filtro por categoría
- Vista de detalles de cada producto
- Botón "Agregar al carrito"

#### **admin.html**
- Panel de control del administrador
- CRUD de categorías
- CRUD de productos
- Gestión de inventario

### Archivos JavaScript

#### **app.js**
Contiene las funciones principales:

- `cargarProductos()` - Obtiene productos de la API
- `cargarCategoriasFiltro()` - Carga categorías para filtros
- `agregarAlCarrito(productoId)` - Agrega producto al carrito
- `funcionesLogin()` - Maneja autenticación
- `funcionesAdmin()` - Funciones del panel admin

### Estilos

#### **styles.css**
- Diseño responsive (mobile-first)
- Paleta de colores profesionales
- Componentes: botones, cards, formularios
- Animaciones suaves

---

## 🗄 Base de Datos

### Diagrama de Relaciones

```
┌─────────────────┐
│   USUARIOS      │
├─────────────────┤
│ id (PK)         │
│ nombre          │
│ email (UNIQUE)  │
│ password        │
│ rol             │
│ created_at      │
└─────────────────┘

┌─────────────────┐
│  CATEGORIAS     │
├─────────────────┤
│ id (PK)         │
│ nombre (UNIQUE) │
│ descripcion     │
└─────────────────┘

┌─────────────────┐
│   PRODUCTOS     │
├─────────────────┤
│ id (PK)         │
│ categoria_id (FK)──→ CATEGORIAS
│ nombre          │
│ precio          │
│ descripcion     │
│ stock           │
│ imagen          │
│ created_at      │
└─────────────────┘
```

### PostgreSQL - DDL Generado Automáticamente

SQLModel crea automáticamente las tablas en PostgreSQL con la estructura anterior cuando se ejecuta:

```python
create_db_and_tables()  # En main.py al iniciar la aplicación
```

---

## ⚙️ Configuración Avanzada

### Variables de Entorno (.env)

```env
# Seguridad
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Base de Datos PostgreSQL
DATABASE_URL=postgresql://ecommerce_user:161901@localhost:5432/ecommerce_db
```

### config.py - Cargue de Configuración

```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
```

### database.py - Conexión a BD

```python
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

---

## 🚨 Manejo de Errores

La API retorna códigos HTTP estándar:

| Código | Significado | Ejemplo |
|--------|------------|---------|
| **200** | OK | Solicitud exitosa |
| **201** | Created | Recurso creado |
| **400** | Bad Request | Email ya existe |
| **401** | Unauthorized | Token inválido/expirado |
| **403** | Forbidden | No tienes permisos (no eres admin) |
| **404** | Not Found | Recurso no encontrado |
| **500** | Server Error | Error del servidor |

### Ejemplo de Respuesta de Error

```json
{
  "detail": "El usuario ya existe"
}
```

---

## 🧪 Testing

### Probar Endpoints Manualmente

#### 1. Registrar Usuario
```bash
curl -X POST "http://localhost:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan", "email": "juan@test.com", "password": "123456"}'
```

#### 2. Iniciar Sesión
```bash
curl -X POST "http://localhost:8000/usuarios/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "juan@test.com", "password": "123456"}'
```

#### 3. Usar Token para Acceder a Endpoints Protegidos
```bash
curl -X GET "http://localhost:8000/usuarios/mi-perfil" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Usar Swagger UI

1. Accede a: http://localhost:8000/docs
2. Haz clic en "Authorize" (candado)
3. Pega tu token JWT
4. Prueba los endpoints interactivamente

---

## 🐛 Solución de Problemas

### Error: "Connection refused" en PostgreSQL

**Solución:** Asegúrate que PostgreSQL esté corriendo:
```bash
docker-compose up -d
docker ps  # Verifica que el contenedor esté activo
```

### Error: "Token inválido" en API

**Solución:** Asegúrate que:
1. El token no ha expirado (30 minutos por defecto)
2. El header esté en el formato correcto: `Authorization: Bearer <token>`
3. La `SECRET_KEY` en `.env` es correcta

### Error: "Usuario no encontrado"

**Solución:** Asegúrate que:
1. La cuenta está registrada correctamente
2. Estás usando el email correcto
3. No hay typos en email o contraseña

### El carrito no persiste (se vacía al recargar)

**Nota:** Es comportamiento normal. El carrito está en memoria. Para persistencia real, necesitarías:
1. Crear tabla `Carrito` en PostgreSQL
2. Asociar carrito a usuario en BD
3. Guardar items en la BD en lugar de en memoria

---

## 📝 Tareas Futuras / Mejoras Sugeridas

- [ ] Persistencia del carrito en base de datos
- [ ] Sistema de pagos (Stripe, PayPal, etc.)
- [ ] Historial de pedidos/facturas
- [ ] Búsqueda avanzada de productos
- [ ] Comentarios y calificaciones
- [ ] Notificaciones por email
- [ ] Recuperación de contraseña
- [ ] Paginación en listados
- [ ] Filtros avanzados (precio, popularidad)
- [ ] Dashboard analítico para admin
- [ ] Tests unitarios e integración

---

## 📞 Soporte y Contacto

Para reportar bugs o sugerir mejoras, por favor abre un issue en el repositorio.

---

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente respetando los términos de la licencia.

---

## 🎓 Recursos Útiles

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [JWT.io](https://jwt.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## 📊 Información del Proyecto

**Creado:** 2026
**Versión:** 1.0.0
**Tipo:** E-commerce de Prendas Deportivas
**Stack:** FastAPI + PostgreSQL + HTML/CSS/JS

---

**Última actualización:** 28 de abril de 2026
