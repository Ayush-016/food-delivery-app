from pydantic import BaseModel, Field
from typing import List, Optional


class OrderItem(BaseModel):
    food_id: str
    name: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class OrderCreate(BaseModel):
    # no input required from user (cart-based order)
    pass


class OrderResponse(BaseModel):
    order_id: str
    total: float
    status: str


class LocationUpdate(BaseModel):
    order_id: str
    lat: float
    lng: float


class OrderTrackResponse(BaseModel):
    status: str
    location: Optional[dict] = None