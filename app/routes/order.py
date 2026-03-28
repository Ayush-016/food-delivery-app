from fastapi import APIRouter, Depends, HTTPException
from app.utils.auth import verify_token
from app.database import db
from bson import ObjectId

from app.models.order import (
    OrderResponse,
    LocationUpdate,
    OrderTrackResponse
)

router = APIRouter()


# ✅ CREATE ORDER
@router.post("/create", response_model=OrderResponse)
def create_order(user=Depends(verify_token)):
    uid = user["email"]

    cart = db.cart.find_one({"user_id": uid})

    if not cart or not cart.get("items"):
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    items = []

    for i in cart["items"]:
        food = db.food.find_one({"_id": ObjectId(i["food_id"])})
        if not food:
            continue

        item_total = food["price"] * i["quantity"]
        total += item_total

        items.append({
            "food_id": i["food_id"],
            "name": food["name"],
            "quantity": i["quantity"],
            "price": food["price"]
        })

    # Save order
    result = db.orders.insert_one({
        "user_id": uid,
        "items": items,
        "total": total,
        "status": "placed",
        "location": None
    })

    # Clear cart
    db.cart.delete_one({"user_id": uid})

    return {
        "order_id": str(result.inserted_id),
        "total": total,
        "status": "placed"
    }


# ✅ UPDATE LOCATION (for delivery tracking)
@router.post("/location")
def update_location(data: LocationUpdate):
    order = db.orders.find_one({"_id": ObjectId(data.order_id)})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.orders.update_one(
        {"_id": ObjectId(data.order_id)},
        {"$set": {"location": {"lat": data.lat, "lng": data.lng}}}
    )

    return {"msg": "Location updated"}


# ✅ TRACK ORDER
@router.get("/track/{order_id}", response_model=OrderTrackResponse)
def track_order(order_id: str):
    order = db.orders.find_one({"_id": ObjectId(order_id)})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "status": order["status"],
        "location": order.get("location")
    }


# ✅ GET USER ORDER HISTORY (IMPORTANT FEATURE)
@router.get("/my-orders")
def get_my_orders(user=Depends(verify_token)):
    uid = user["email"]

    orders = list(db.orders.find({"user_id": uid}))

    for o in orders:
        o["_id"] = str(o["_id"])

    return orders