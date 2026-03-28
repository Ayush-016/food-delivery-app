from fastapi import APIRouter, Depends, UploadFile, File
from app.utils.auth import admin_required
from app.database import db
from app.utils.image import save_image
from app.models.food import FoodCreate

router = APIRouter()

@router.post("/add-food")
async def add_food(
    food: FoodCreate = Depends(),
    image: UploadFile = File(...),
    user=Depends(admin_required)
):
    img = save_image(image)

    db.food.insert_one({
        "name": food.name,
        "description": food.description,
        "price": food.price,
        "image_url": img
    })

    return {"msg": "Food added"}

@router.get("/foods")
def get_foods():
    return list(db.food.find({}, {"_id": 0}))