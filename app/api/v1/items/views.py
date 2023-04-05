from fastapi import HTTPException, Depends, APIRouter
from bson import ObjectId
from models.items import Items
from config import project_db
from auth.auth import get_current_user
from typing import List

router = APIRouter()

# Connect to MongoDB
collection = project_db['mycollection']

# Define the schema for a document in the collection


@router.get("", dependencies=[Depends(get_current_user)])
async def read_items():
    items = []
    for item in collection.find():
        items.append(
            {
                "id": str(item['_id']),
                "name": item['name'],
                "description": item['description']
            }
        )
    return items


@router.get("/{item_id}")
async def read_item(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "id": str(item['_id']),
        "name": item['name'],
        "description": item['description']
    }


@router.post("", response_model=Items)
async def create_item(item: Items):
    item_dict = item.dict()
    # item_dict.pop("_id")  # Removing "_id" field from the dictionary
    new_item = collection.insert_one(item_dict)
    item_id = new_item.inserted_id
    created_item = collection.find_one({"_id": item_id})
    return created_item


@router.put("/{item_id}")
async def update_item(item_id: str, item: Items):
    result = collection.update_one(
        {"_id": ObjectId(item_id)}, {"$set": item.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item updated successfully"}


@router.delete("/{item_id}")
async def delete_item(item_id: str):
    result = collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
