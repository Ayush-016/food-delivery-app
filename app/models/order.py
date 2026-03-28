from pydantic import BaseModel, Field
from typing import Optional


# ✅ Response when order is created
class OrderResponse(BaseModel):
    order_id: str
    total: float
    status: str


# ✅ For updating delivery location
class LocationUpdate(BaseModel):
    order_id: str
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


# ✅ For tracking response
class OrderTrackResponse(BaseModel):
    status: str
    location: Optional[dict] = None