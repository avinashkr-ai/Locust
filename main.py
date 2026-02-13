from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import database as db

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.on_event("startup")
async def startup_event():
    """Check if database exists on startup"""
    if not os.path.exists(db.DB_PATH):
        print("\n" + "="*60)
        print("⚠️  WARNING: Database not found!")
        print("="*60)
        print("Please run the database initialization script first:")
        print("  python db_init.py")
        print("="*60 + "\n")

@app.get("/")
def root():
    """Health check endpoint"""
    try:
        total_items = db.get_item_count()
        return {
            "status": "API is running",
            "database": "connected",
            "total_items": total_items
        }
    except Exception as e:
        return {
            "status": "API is running",
            "database": "error",
            "error": str(e),
            "message": "Please run: python db_init.py"
        }

@app.get("/items/")
def read_all(skip: int = 0, limit: int = 100):
    """
    Get items from database with pagination.
    Defaults to the first 100 items to keep responses fast under heavy load.
    """
    try:
        items = db.get_all_items(skip=skip, limit=limit)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """Get a specific item by ID"""
    try:
        item = db.get_item_by_id(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/items/")
def create_item(item: Item):
    """Create a new item"""
    try:
        new_item = db.create_item(item.name, item.price)
        return new_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Update an existing item"""
    try:
        updated_item = db.update_item(item_id, item.name, item.price)
        if updated_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item"""
    try:
        deleted = db.delete_item(item_id)
        if deleted:
            return {"message": "Item deleted successfully", "item_id": item_id}
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
