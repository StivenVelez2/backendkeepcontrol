from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import init_db, SessionLocal, Producto, Venta, DetalleVenta, Devolucion
from app.schemas import (
    ProductoCreate, ProductoResponse,
    VentaCreate, VentaResponse,
    DevolucionCreate, DevolucionResponse,
    DashboardResponse,
)
from app.seed import seed_database

app = FastAPI(title="K Bonita - Keep Control API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup():
    init_db()
    seed_database()


# ─── PRODUCTOS ───────────────────────────────────────────────

@app.get("/productos", response_model=List[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()


@app.get("/productos/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod


@app.put("/productos/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto: ProductoCreate, db: Session = Depends(get_db)):
    prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in producto.model_dump().items():
        setattr(prod, key, value)
    db.commit()
    db.refresh(prod)
    return prod


@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(prod)
    db.commit()


@app.post("/productos", response_model=ProductoResponse, status_code=201)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    prod = Producto(**producto.model_dump())
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod


# ─── VENTAS ──────────────────────────────────────────────────

@app.get("/ventas", response_model=List[VentaResponse])
def listar_ventas(db: Session = Depends(get_db)):
    return db.query(Venta).all()


@app.get("/ventas/{venta_id}", response_model=VentaResponse)
def obtener_venta(venta_id: int, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(Venta.id == venta_id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta


@app.post("/ventas", response_model=VentaResponse, status_code=201)
def crear_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    for det in venta.detalles:
        producto = db.query(Producto).filter(Producto.id == det.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto id={det.producto_id} no encontrado")
        if producto.stock < det.cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}")
        producto.stock -= det.cantidad

    db_venta = Venta(total=venta.total)
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)

    for det in venta.detalles:
        db.add(DetalleVenta(
            venta_id=db_venta.id,
            producto_id=det.producto_id,
            cantidad=det.cantidad,
            precio_unitario=det.precio_unitario,
            subtotal=det.subtotal,
        ))
    db.commit()
    db.refresh(db_venta)
    return db_venta


# ─── DEVOLUCIONES ────────────────────────────────────────────

@app.get("/devoluciones", response_model=List[DevolucionResponse])
def listar_devoluciones(db: Session = Depends(get_db)):
    return db.query(Devolucion).all()


@app.get("/devoluciones/{devolucion_id}", response_model=DevolucionResponse)
def obtener_devolucion(devolucion_id: int, db: Session = Depends(get_db)):
    dev = db.query(Devolucion).filter(Devolucion.id == devolucion_id).first()
    if not dev:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")
    return dev


@app.post("/devoluciones", response_model=DevolucionResponse, status_code=201)
def crear_devolucion(devolucion: DevolucionCreate, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(Venta.id == devolucion.venta_id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    producto = db.query(Producto).filter(Producto.id == devolucion.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db_dev = Devolucion(**devolucion.model_dump())
    db.add(db_dev)

    producto.stock += devolucion.cantidad

    db.commit()
    db.refresh(db_dev)
    return db_dev


# ─── DASHBOARD ───────────────────────────────────────────────

@app.get("/dashboard", response_model=DashboardResponse)
def dashboard(db: Session = Depends(get_db)):
    total_productos = db.query(func.count(Producto.id)).scalar() or 0
    total_ventas = db.query(func.count(Venta.id)).scalar() or 0
    ingresos_totales = db.query(func.coalesce(func.sum(Venta.total), 0)).scalar() or 0
    total_devoluciones = db.query(func.count(Devolucion.id)).scalar() or 0

    productos_mas_vendidos = (
        db.query(
            Producto.nombre,
            func.sum(DetalleVenta.cantidad).label("total_vendido"),
        )
        .join(DetalleVenta, DetalleVenta.producto_id == Producto.id)
        .group_by(Producto.id)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .limit(5)
        .all()
    )

    ventas_por_dia = (
        db.query(
            func.date(Venta.fecha).label("dia"),
            func.sum(Venta.total).label("total"),
        )
        .group_by(func.date(Venta.fecha))
        .order_by(func.date(Venta.fecha).desc())
        .limit(7)
        .all()
    )

    return DashboardResponse(
        total_productos=total_productos,
        total_ventas=total_ventas,
        ingresos_totales=ingresos_totales,
        total_devoluciones=total_devoluciones,
        productos_mas_vendidos=[
            {"nombre": p.nombre, "total_vendido": p.total_vendido}
            for p in productos_mas_vendidos
        ],
        ventas_por_dia=[
            {"dia": str(v.dia), "total": v.total}
            for v in ventas_por_dia
        ],
    )
