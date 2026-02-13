"""
Database utility functions for SQLite connection and operations
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

DB_PATH = "products.db"

@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    Automatically handles connection opening and closing
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    finally:
        conn.close()

def get_all_items() -> List[Dict[str, Any]]:
    """Get all items from database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM items ORDER BY id")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_item_by_id(item_id: int) -> Optional[Dict[str, Any]]:
    """Get a single item by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def create_item(name: str, price: float) -> Dict[str, Any]:
    """Create a new item"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, price) VALUES (?, ?)",
            (name, price)
        )
        conn.commit()
        new_id = cursor.lastrowid
        return {"id": new_id, "name": name, "price": price}

def update_item(item_id: int, name: str, price: float) -> Optional[Dict[str, Any]]:
    """Update an existing item"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE items SET name = ?, price = ? WHERE id = ?",
            (name, price, item_id)
        )
        conn.commit()
        
        if cursor.rowcount > 0:
            return {"id": item_id, "name": name, "price": price}
        return None

def delete_item(item_id: int) -> bool:
    """Delete an item by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_item_count() -> int:
    """Get total count of items"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        return cursor.fetchone()[0]
