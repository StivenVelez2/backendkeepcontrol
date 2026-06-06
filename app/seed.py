from app.database import SessionLocal, Producto

PRODUCTOS_INICIALES = [
    {"nombre": "Blusa Lisa", "descripcion": "Blusa de algodón lisa, fresca y cómoda", "precio": 25.99, "stock": 50, "talla": "M", "color": "Blanco", "categoria": "Blusas"},
    {"nombre": "Vestido Floral", "descripcion": "Vestido estampado floral con vuelo", "precio": 45.50, "stock": 30, "talla": "S", "color": "Rosado", "categoria": "Vestidos"},
    {"nombre": "Jean Clásico", "descripcion": "Jean de corte recto clásico", "precio": 39.99, "stock": 40, "talla": "L", "color": "Azul", "categoria": "Pantalones"},
    {"nombre": "Chaqueta de Cuero", "descripcion": "Chaqueta de cuero sintético moderna", "precio": 89.99, "stock": 20, "talla": "M", "color": "Negro", "categoria": "Chaquetas"},
    {"nombre": "Falda Plisada", "descripcion": "Falda plisada larga, elegante", "precio": 34.99, "stock": 35, "talla": "S", "color": "Verde", "categoria": "Faldas"},
    {"nombre": "Camisa Manga Larga", "descripcion": "Camisa formal de manga larga", "precio": 29.99, "stock": 45, "talla": "L", "color": "Celeste", "categoria": "Camisas"},
    {"nombre": "Short Deportivo", "descripcion": "Short deportivo de algodón", "precio": 19.99, "stock": 60, "talla": "M", "color": "Gris", "categoria": "Shorts"},
    {"nombre": "Suéter de Lana", "descripcion": "Suéter tejido de lana suave", "precio": 55.00, "stock": 25, "talla": "XL", "color": "Café", "categoria": "Suéteres"},
    {"nombre": "Top Deportivo", "descripcion": "Top deportivo ajustable", "precio": 22.50, "stock": 55, "talla": "S", "color": "Morado", "categoria": "Deportivo"},
    {"nombre": "Cargo Pantalón", "descripcion": "Pantalón cargo con bolsillos laterales", "precio": 42.00, "stock": 30, "talla": "L", "color": "Oliva", "categoria": "Pantalones"},
]


def seed_database():
    db = SessionLocal()
    try:
        existentes = db.query(Producto).count()
        if existentes == 0:
            for prod in PRODUCTOS_INICIALES:
                db.add(Producto(**prod))
            db.commit()
            print("Base de datos inicializada con 10 productos de ejemplo.")
        else:
            print(f"Base de datos ya contiene {existentes} productos. Omitiendo seed.")
    finally:
        db.close()
