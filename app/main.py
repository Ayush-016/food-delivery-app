import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import auth, food, cart, order

app = FastAPI()

# ✅ create uploads folder if not exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.include_router(auth.router, prefix="/auth")
app.include_router(food.router, prefix="/food")
app.include_router(cart.router, prefix="/cart")
app.include_router(order.router, prefix="/order")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def home():
    return {"message": "API running"}

