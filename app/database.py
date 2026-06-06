from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./keep_control.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, default="")
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    talla = Column(String(10), default="")
    color = Column(String(50), default="")
    categoria = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    detalle_ventas = relationship("DetalleVenta", back_populates="producto")
    devoluciones = relationship("Devolucion", back_populates="producto")


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float, nullable=False, default=0)
    fecha = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    detalle_ventas = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
    devoluciones = relationship("Devolucion", back_populates="venta")


class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    venta = relationship("Venta", back_populates="detalle_ventas")
    producto = relationship("Producto", back_populates="detalle_ventas")


class Devolucion(Base):
    __tablename__ = "devoluciones"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    motivo = Column(Text, default="")
    fecha = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    venta = relationship("Venta", back_populates="devoluciones")
    producto = relationship("Producto", back_populates="devoluciones")


def init_db():
    Base.metadata.create_all(bind=engine)
