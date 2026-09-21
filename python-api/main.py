from datetime import datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from auth_schemas import LoginRequest, SignupRequest, UserResponse
from database import Base, engine, get_db
from models import Booking
from user_models import User


app = FastAPI(
    title="Laundry Business API",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


security = HTTPBearer()


# ============================================================
# BOOKING SCHEMAS
# ============================================================

class BookingCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    address: str
    service: str
    pickup_date: str
    pickup_time: str
    details: Optional[str] = None


# ============================================================
# AUTHENTICATION
# ============================================================

@app.post("/signup")
def signup(
    user_data: SignupRequest,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        role="customer",
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Account created successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role
        }
    }


@app.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    access_token = create_access_token(user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role
        }
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user_id = decode_access_token(credentials.credentials)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    return user


@app.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


# ============================================================
# GENERAL
# ============================================================

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


# ============================================================
# BOOKINGS
# ============================================================

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