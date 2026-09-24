from typing import Optional

from pydantic import BaseModel


class OrderCreate(BaseModel):
    pickup_address: str
    pickup_date: str
    pickup_time: str
    delivery_date: Optional[str] = None
    service: str
    special_instructions: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    pickup_address: str
    pickup_date: str
    pickup_time: str
    delivery_date: Optional[str]
    service: str
    special_instructions: Optional[str]
    status: str
    total_price: Optional[str]

    class Config:
        from_attributes = True
