from pydantic import BaseModel, Field

class FoodCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str = Field(min_length=5)
    price: float = Field(gt=0)