from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    contact = Column(String(250))
    rating = Column(Numeric(2, 1), default=0)

    orders = relationship("PurchaseOrder", back_populates="vendor")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    stock_level = Column(Integer, default=0)

    po_items = relationship("POItem", back_populates="product")


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    reference_no = Column(String(50), unique=True, nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    total_amount = Column(Numeric(12, 2), default=0)
    status = Column(String(20), default="DRAFT")

    vendor = relationship("Vendor", back_populates="orders")
    items = relationship("POItem", back_populates="order")


class POItem(Base):
    __tablename__ = "po_items"

    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product", back_populates="po_items")