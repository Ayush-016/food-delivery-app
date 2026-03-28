from fastapi import APIRouter, HTTPException
from app.database import db
from app.utils.auth import hash_password, verify_password, create_token
from app.models.user import UserRegister, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------- REGISTER ----------------
@router.post("/register")
def register(user: UserRegister):
    existing = db.users.find_one({"email": user.email})

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    db.users.insert_one({
        "email": user.email,
        "password": hash_password(user.password),
        "role": "user"   # default role
    })

    return {"msg": "Registered successfully"}


# ---------------- LOGIN ----------------
@router.post("/login")
def login(user: UserLogin):
    db_user = db.users.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # ✅ TOKEN PAYLOAD
    payload = {
        "email": db_user["email"],
        "role": db_user.get("role", "user")
    }

    token = create_token(payload)

    return {
        "access_token": token,                
        "role": db_user.get("role", "user")  
    }