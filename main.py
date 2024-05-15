from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory database to store items
items_db: Dict[int, dict] = {}

# Pydantic model for Item
class Item(BaseModel):
    name: str
    description: str
    price: float

# Endpoint to create a new item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    item_id = len(items_db) + 1
    items_db[item_id] = item.dict()
    return item

# Endpoint to get an item by ID
@app.get("/items/{item_id}/", response_model=Item)
async def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

# Endpoint to update an item by ID
@app.put("/items/{item_id}/", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item.dict()
    return item

# Endpoint to delete an item by ID
@app.delete("/items/{item_id}/", response_model=dict)
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)
    return {"message": "Item deleted", "deleted_item": deleted_item}

# Endpoint to get all items
@app.get("/items/", response_model=list)
async def read_items():
    return list(items_db.values())
