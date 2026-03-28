from pydantic import BaseModel

class Food(BaseModel):
    name: str
    category: str
    price: float
    image : str