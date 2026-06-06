# K Bonita - Keep Control API

Backend REST para el sistema de inventario y ventas de la tienda de ropa **K Bonita**.

## Tecnologías

- Python 3.10+
- FastAPI
- SQLite (via SQLAlchemy)
- Uvicorn

## Instalación

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/macOS

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar servidor
uvicorn app.main:app --reload
```

El servidor se iniciará en `http://localhost:8000`.

## Documentación interactiva

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

| Método | Ruta                | Descripción                    |
|--------|---------------------|--------------------------------|
| GET    | /productos          | Listar todos los productos     |
| GET    | /productos/{id}     | Obtener un producto por ID     |
| POST   | /productos          | Crear un nuevo producto        |
| GET    | /ventas             | Listar todas las ventas        |
| GET    | /ventas/{id}        | Obtener una venta por ID       |
| POST   | /ventas             | Crear una nueva venta          |
| GET    | /devoluciones       | Listar todas las devoluciones  |
| GET    | /devoluciones/{id}  | Obtener una devolución por ID  |
| POST   | /devoluciones       | Crear una nueva devolución     |
| GET    | /dashboard          | Resumen general del negocio    |

## Base de datos

El archivo `keep_control.db` se crea automáticamente al iniciar el servidor.
Si la base está vacía, se insertan 10 productos de ejemplo de ropa.

### Tablas

- **productos**: Catálogo de prendas (nombre, precio, stock, talla, color, categoría)
- **ventas**: Cabecera de cada venta
- **detalle_ventas**: Productos incluidos en cada venta
- **devoluciones**: Registro de devoluciones
