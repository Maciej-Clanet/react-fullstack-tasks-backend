from bson import ObjectId
from fastapi import HTTPException
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["fullstack_tasks"]


# The following function is useful when dealing with mongodb ID's
# Since we cant give monogo a string for an ID without it exploding...
def to_object_id(id_str: str) -> ObjectId:
    """
    Safely convert a string like '67123abc...' into a MongoDB ObjectId.
    If it's not a valid hex string, we raise a 400 error for the client.
    """
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")


# This is also useful so we wont have to manually convert the id every time when we want the entire document
def serialize_doc(doc: dict) -> dict:
    """
    Convert MongoDB document (which has _id: ObjectId) into a JSON-safe dict
    where _id is a string. This makes FastAPI happy when returning JSON.
    """
    if not doc:
        return doc
    doc["_id"] = str(doc["_id"])
    return doc
