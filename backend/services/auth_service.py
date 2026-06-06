from datetime import datetime

from backend.database.collections import users_collection
from backend.auth.password import (
    hash_password,
    verify_password
)
from backend.auth.jwt_handler import (
    create_access_token
)


def register_user(name, email, password):

    existing_user = users_collection.find_one(
        {"email": email}
    )

    if existing_user:
        raise Exception("Email already registered")

    hashed_password = hash_password(password)

    user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": "user",
        "created_at": datetime.utcnow()
    }

    users_collection.insert_one(user)

    return {
        "message": "User registered successfully"
    }


def login_user(email, password):

    user = users_collection.find_one(
        {"email": email}
    )

    if not user:
        raise Exception("Invalid credentials")

    is_valid = verify_password(
        password,
        user["password"]
    )

    if not is_valid:
        raise Exception("Invalid credentials")

    token = create_access_token({
        "user_id": str(user["_id"]),
        "email": user["email"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }