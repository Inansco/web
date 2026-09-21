from sqlalchemy import Column, Integer, String, Text
from database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(150), nullable=True)
    address = Column(Text, nullable=False)
    service = Column(String(100), nullable=False)
    pickup_date = Column(String(20), nullable=False)
    pickup_time = Column(String(20), nullable=False)
    details = Column(Text, nullable=True)
    status = Column(String(30), nullable=False, default="Pending")
    created_at = Column(String(50), nullable=False)