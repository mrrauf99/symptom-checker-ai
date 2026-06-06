from bson import ObjectId

from backend.database.collections import (
    users_collection
)


def get_profile(user_id):

    user = users_collection.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )

    if not user:
        return None

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user.get("age"),
        "gender": user.get("gender")
    }


def update_profile(
    user_id,
    data
):

    users_collection.update_one(
        {
            "_id": ObjectId(user_id)
        },
        {
            "$set": {
                "name": data.name,
                "age": data.age,
                "gender": data.gender
            }
        }
    )

    user = users_collection.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user.get("age"),
        "gender": user.get("gender")
    }