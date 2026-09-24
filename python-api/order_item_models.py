from sqlalchemy import Column, ForeignKey, Integer, String, Text

from database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )

    item_name = Column(
        String(100),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )

    notes = Column(
        Text,
        nullable=True
    )

    price = Column(
        String(30),
        nullable=True
    )
