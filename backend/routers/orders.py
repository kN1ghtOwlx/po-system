from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import PurchaseOrder, POItem
from schemas import POCreate, POOut
from typing import List
import uuid

router = APIRouter(prefix="/orders", tags=["Orders"])

TAX_RATE = 0.05

def calculate_total(db: Session, po_id: int):
    items = db.query(POItem).filter(POItem.po_id == po_id).all()
    subtotal = sum(item.quantity * item.unit_price for item in items)
    total = round(subtotal * (1 + TAX_RATE), 2)
    db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id)\
        .update({"total_amount": total})
    db.commit()
    return total

@router.get("/", response_model=List[POOut])
def get_orders(db: Session = Depends(get_db)):
    return db.query(PurchaseOrder).all()

@router.post("/", response_model=POOut)
def create_order(po: POCreate, db: Session = Depends(get_db)):
    ref_no = "PO-" + str(uuid.uuid4())[:8].upper()
    new_po = PurchaseOrder(reference_no=ref_no, vendor_id=po.vendor_id)
    db.add(new_po)
    db.commit()
    db.refresh(new_po)

    for item in po.items:
        po_item = POItem(
            po_id=new_po.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        db.add(po_item)
    db.commit()

    calculate_total(db, new_po.id)
    db.refresh(new_po)
    return new_po

@router.patch("/{order_id}/status")
def update_status(order_id: int, status: str, db: Session = Depends(get_db)):
    valid = ["DRAFT", "SUBMITTED", "APPROVED", "REJECTED"]
    if status not in valid:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid}")
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    return {"message": f"Status updated to {status}"}