from pydantic import BaseModel

class CartAdd(BaseModel):
    food_id: str