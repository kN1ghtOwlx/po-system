from database import SessionLocal
from models import Vendor, Product, PurchaseOrder, POItem

db = SessionLocal()

vendors = [
    Vendor(name="TechSupplies Co", contact="tech@supplies.com", rating=4.5),
    Vendor(name="Office Depot Pro", contact="sales@officedepot.com", rating=3.8),
    Vendor(name="Global Parts Ltd", contact="info@globalparts.com", rating=4.2),
]

products = [
    Product(name="Laptop Stand", sku="SKU-001", unit_price=29.99, stock_level=100),
    Product(name="Wireless Mouse", sku="SKU-002", unit_price=19.99, stock_level=200),
    Product(name="USB Hub", sku="SKU-003", unit_price=14.99, stock_level=150),
    Product(name="Monitor Cable", sku="SKU-004", unit_price=9.99, stock_level=300),
    Product(name="Keyboard", sku="SKU-005", unit_price=49.99, stock_level=80),
]

db.add_all(vendors)
db.add_all(products)
db.commit()
db.close()

print("Seed data inserted successfully")