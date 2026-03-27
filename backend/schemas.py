from pydantic import BaseModel
from typing import Optional, List

class VendorCreate(BaseModel):
    name: str
    contact: Optional[str] = None
    rating: Optional[float] = 0

class VendorOut(BaseModel):
    id: int
    name: str
    contact: Optional[str]
    rating: Optional[float]

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    sku: str
    unit_price: float
    stock_level: Optional[int] = 0

class ProductOut(BaseModel):
    id: int
    name: str
    sku: str
    unit_price: float
    stock_level: int

    class Config:
        from_attributes = True


class POItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class POCreate(BaseModel):
    vendor_id: int
    items: List[POItemCreate]

class POOut(BaseModel):
    id: int
    reference_no: str
    vendor_id: int
    total_amount: float
    status: str

    class Config:
        from_attributes = True