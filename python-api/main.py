from datetime import datetime
from typing import Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Booking


app = FastAPI(
    title="Laundry Business API",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


class BookingCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    address: str
    service: str
    pickup_date: str
    pickup_time: str
    details: Optional[str] = None


@app.get("/")
def home():
    return {
        "message": "Laundry API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/bookings")
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db)
):
    booking = Booking(
        name=booking_data.name,
        phone=booking_data.phone,
        email=booking_data.email,
        address=booking_data.address,
        service=booking_data.service,
        pickup_date=booking_data.pickup_date,
        pickup_time=booking_data.pickup_time,
        details=booking_data.details,
        status="Pending",
        created_at=datetime.now().isoformat()
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking created successfully",
        "booking": {
            "id": booking.id,
            "name": booking.name,
            "phone": booking.phone,
            "email": booking.email,
            "address": booking.address,
            "service": booking.service,
            "pickup_date": booking.pickup_date,
            "pickup_time": booking.pickup_time,
            "details": booking.details,
            "status": booking.status,
            "created_at": booking.created_at
        }
    }


@app.get("/bookings")
def get_bookings(
    db: Session = Depends(get_db)
):
    bookings = (
        db.query(Booking)
        .order_by(Booking.id.desc())
        .all()
    )

    return {
        "total": len(bookings),
        "bookings": [
            {
                "id": booking.id,
                "name": booking.name,
                "phone": booking.phone,
                "email": booking.email,
                "address": booking.address,
                "service": booking.service,
                "pickup_date": booking.pickup_date,
                "pickup_time": booking.pickup_time,
                "details": booking.details,
                "status": booking.status,
                "created_at": booking.created_at
            }
            for booking in bookings
        ]
    }