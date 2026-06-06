from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductoBase(BaseModel):
    nombre: str
    descripcion: str = ""
    precio: float
    stock: int = 0
    talla: str = ""
    color: str = ""
    categoria: str = ""


class ProductoCreate(ProductoBase):
    pass


class ProductoResponse(ProductoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DetalleVentaBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float


class DetalleVentaResponse(DetalleVentaBase):
    id: int
    venta_id: int

    class Config:
        from_attributes = True


class VentaBase(BaseModel):
    total: float
    detalles: List[DetalleVentaBase]


class VentaCreate(VentaBase):
    pass


class VentaResponse(BaseModel):
    id: int
    total: float
    fecha: datetime
    created_at: datetime
    detalle_ventas: List[DetalleVentaResponse] = []

    class Config:
        from_attributes = True


class DevolucionBase(BaseModel):
    venta_id: int
    producto_id: int
    cantidad: int
    motivo: str = ""


class DevolucionCreate(DevolucionBase):
    pass


class DevolucionResponse(DevolucionBase):
    id: int
    fecha: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    total_productos: int
    total_ventas: int
    ingresos_totales: float
    total_devoluciones: int
    productos_mas_vendidos: List[dict]
    ventas_por_dia: List[dict]
