from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(
    title="Laundry Business API",
    version="1.0.0"
)


class Booking(BaseModel):
    name: str
    phone: str
    email: str | None = None
    address: str
    service: str
    pickup_date: str
    pickup_time: str
    details: str | None = None


bookings: List[dict] = []


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
def create_booking(booking: Booking):

    booking_data = booking.model_dump()

    booking_data["id"] = len(bookings) + 1
    booking_data["status"] = "Pending"
    booking_data["created_at"] = datetime.now().isoformat()

    bookings.append(booking_data)

    return {
        "message": "Booking created successfully",
        "booking": booking_data
    }


@app.get("/bookings")
def get_bookings():
    return {
        "total": len(bookings),
        "bookings": bookings
    }