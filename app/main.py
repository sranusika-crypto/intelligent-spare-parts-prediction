
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import engine, Base, SessionLocal
from app.models import SparePart

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Intelligent Industrial Spare Parts Demand Prediction Platform",
    description="Manage spare parts inventory and low-stock alerts.",
    version="1.0.0"
)


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Spare Parts Demand Prediction Platform",
        "status": "Application is running"
    }


# View all spare parts
@app.get("/spare-parts")
def get_spare_parts(db: Session = Depends(get_db)):
    return db.query(SparePart).all()


# Add a new spare part
@app.post("/spare-parts")
def add_spare_part(
    name: str,
    stock: int,
    criticality: str = "Medium",
    db: Session = Depends(get_db)
):
    if stock < 0:
        raise HTTPException(
            status_code=400,
            detail="Stock cannot be negative"
        )

    part = SparePart(
        name=name,
        stock=stock,
        criticality=criticality
    )

    db.add(part)
    db.commit()
    db.refresh(part)

    return {
        "message": "Spare part added successfully",
        "spare_part": part
    }


# View low-stock alerts
@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    low_stock_parts = (
        db.query(SparePart)
        .filter(SparePart.stock < 10)
        .all()
    )

    return {
        "alert_count": len(low_stock_parts),
        "message": "Low-stock spare parts",
        "alerts": low_stock_parts
    }


# View inventory summary
@app.get("/inventory-summary")
def inventory_summary(db: Session = Depends(get_db)):
    total_parts = db.query(SparePart).count()

    total_stock = (
        db.query(func.sum(SparePart.stock)).scalar() or 0
    )

    low_stock_count = (
        db.query(SparePart)
        .filter(SparePart.stock < 10)
        .count()
    )

    return {
        "total_part_types": total_parts,
        "total_stock_quantity": total_stock,
        "low_stock_part_types": low_stock_count
    }
