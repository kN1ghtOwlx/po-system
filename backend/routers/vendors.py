from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Vendor
from schemas import VendorCreate, VendorOut
from typing import List

router = APIRouter(prefix="/vendors", tags=["Vendors"])

@router.get("/", response_model=List[VendorOut])
def get_vendors(db: Session = Depends(get_db)):
    return db.query(Vendor).all()

@router.post("/", response_model=VendorOut)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    new_vendor = Vendor(**vendor.model_dump())
    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor

@router.delete("/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    db.delete(vendor)
    db.commit()
    return {"message": "Vendor deleted"}