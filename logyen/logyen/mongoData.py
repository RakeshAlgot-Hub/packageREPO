from .config import MongoConfig


def findUser(email: str):
    try:
        if MongoConfig.collection is None:
            raise ValueError("MongoConfig is not configured. Call MongoConfig.configure() first.")
        return MongoConfig.collection.find_one({"email": email})
    except Exception as e:
        print(f"Error finding user: {e}")
        return None