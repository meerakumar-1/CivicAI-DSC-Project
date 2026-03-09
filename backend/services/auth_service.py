from datetime import datetime
from fastapi import HTTPException
from database import users_collection

from utils.hashing import hash_password, verify_password
from utils.jwt_handler import create_access_token


async def signup_user(user):

    existing_user = await users_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "locality": user.locality,
        "role": "user",
        "created_at": datetime.utcnow()
    }

    result = await users_collection.insert_one(new_user)

    token = create_access_token({
        "user_id": str(result.inserted_id)
    })

    return token


async def login_user(user):

    db_user = await users_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": str(db_user["_id"])
    })

    return token