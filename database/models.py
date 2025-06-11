from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Таблица связи между материалами и продукцией
material_product = Table('material_product', Base.metadata,
                         Column('material_id', Integer, ForeignKey('materials.id')),
                         Column('product_id', Integer, ForeignKey('products.id')),
                         Column('quantity', Float)  # Количество материала на единицу продукции
                         )


class MaterialType(Base):
    __tablename__ = 'material_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    materials = relationship("Material", back_populates="type")


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('material_types.id'))
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    package_quantity = Column(Float, nullable=True)
    stock_quantity = Column(Float, nullable=True)
    min_quantity = Column(Float, nullable=True)

    type = relationship("MaterialType", back_populates="materials")
    products = relationship("Product", secondary=material_product, back_populates="materials")


class ProductType(Base):
    __tablename__ = 'product_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    coefficient = Column(Float, nullable=False)  # Коэффициент типа продукции
    products = relationship("Product", back_populates="type")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('product_types.id'))
    name = Column(String, nullable=False)
    article = Column(String, nullable=False, unique=True)
    min_partner_price = Column(Float, nullable=True)
    quantity = Column(Float, nullable=True, default=0.0)  # Добавляем поле quantity

    type = relationship("ProductType", back_populates="products")
    materials = relationship("Material", secondary=material_product, back_populates="products")