from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    pickup_address = Column(
        Text,
        nullable=False
    )

    pickup_date = Column(
        String(20),
        nullable=False
    )

    pickup_time = Column(
        String(20),
        nullable=False
    )

    delivery_date = Column(
        String(20),
        nullable=True
    )

    service = Column(
        String(100),
        nullable=False
    )

    special_instructions = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="BOOKED"
    )

    total_price = Column(
        String(30),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
