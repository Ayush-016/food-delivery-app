from fastapi import APIRouter, Depends
from app.utils.auth import verify_token
from app.database import db

router = APIRouter()

@router.post("/cart/add")
def add_to_cart(food_id: str, user=Depends(verify_token)):
    uid = user["email"]

    res = db.cart.update_one(
        {"user_id": uid, "items.food_id": food_id},
        {"$inc": {"items.$.quantity": 1}}
    )

    if res.matched_count == 0:
        db.cart.update_one(
            {"user_id": uid},
            {"$push": {"items": {"food_id": food_id, "quantity": 1}}},
            upsert=True
        )

    return {"msg": "Cart updated"}

@router.get("/cart")
def get_cart(user=Depends(verify_token)):
    return db.cart.find_one({"user_id": user["email"]}, {"_id": 0})