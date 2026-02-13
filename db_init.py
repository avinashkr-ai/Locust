#!/usr/bin/env python3
"""
Database Initialization Script
Creates the SQLite database and populates it with seed data
Run this BEFORE starting the FastAPI server
"""

import sqlite3
import os
import random

# Database file path
DB_PATH = "products.db"

# Generate 50000 seed data items using for loop
SEED_DATA = []

# Product categories for variety
categories = ["Keyboard", "Mouse", "Monitor", "Headphones", "Speaker", "Webcam", "Laptop", 
              "Tablet", "Smartphone", "Smartwatch", "Router", "Switch", "Cable", "Adapter",
              "Charger", "Battery", "SSD", "HDD", "RAM", "Processor", "Graphics Card",
              "Motherboard", "Case", "Cooling Fan", "PSU", "Chair", "Desk", "Lamp",
              "Microphone", "Camera", "Printer", "Scanner", "TV", "Projector", "Drone",
              "VR Headset", "Controller", "Hub", "Dock", "Stand"]

# Generate 50000 items using for loop
for i in range(1, 50001):
    # Select category (cycle through categories)
    category = categories[(i - 1) % len(categories)]
    
    # Create product name with variation
    product_name = f"{category} Model {i}"
    
    # Generate price based on item number (creates variety)
    # Prices range from $9.99 to $1999.99
    base_price = 10 + (i % 1990)
    price = round(base_price + random.uniform(0, 9.99), 2)
    
    SEED_DATA.append({
        "id": i,
        "name": product_name,
        "price": price
    })

def create_database():
    """Create the database and items table"""
    print("🔧 Creating database...")
    
    # Remove existing database if it exists
    if os.path.exists(DB_PATH):
        print(f"   ⚠️  Removing existing database: {DB_PATH}")
        os.remove(DB_PATH)
    
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    print(f"   ✅ Database created: {DB_PATH}")
    print(f"   ✅ Table 'items' created")
    
    return conn, cursor

def insert_seed_data(conn, cursor):
    """Insert seed data into the database"""
    print("\n📦 Inserting seed data...")
    
    # Insert seed data
    for item in SEED_DATA:
        cursor.execute(
            "INSERT INTO items (id, name, price) VALUES (?, ?, ?)",
            (item["id"], item["name"], item["price"])
        )
    
    conn.commit()
    print(f"   ✅ Inserted {len(SEED_DATA)} items")

def verify_data(cursor):
    """Verify that data was inserted correctly"""
    print("\n🔍 Verifying data...")
    
    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]
    print(f"   ✅ Total items in database: {count}")
    
    cursor.execute("SELECT id, name, price FROM items LIMIT 5")
    sample_items = cursor.fetchall()
    print("\n   📋 Sample items:")
    for item in sample_items:
        print(f"      ID: {item[0]}, Name: {item[1]}, Price: ${item[2]:.2f}")

def main():
    """Main function to initialize the database"""
    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)
    print()
    
    try:
        # Create database and table
        conn, cursor = create_database()
        
        # Insert seed data
        insert_seed_data(conn, cursor)
        
        # Verify data
        verify_data(cursor)
        
        # Close connection
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ DATABASE INITIALIZATION COMPLETE!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Start the FastAPI server: uvicorn main:app --reload")
        print("2. Run load tests: locust -f locustfile.py --host=http://localhost:8000")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())