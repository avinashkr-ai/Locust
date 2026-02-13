# 🗄️ Database Setup Guide

## Overview

This project now uses **SQLite** for persistent data storage instead of an in-memory dictionary. This means:

✅ Data persists between server restarts
✅ Real-world database performance testing
✅ Learn SQL and database optimization
✅ Easy to upgrade to PostgreSQL/MySQL later

---

## What Changed?

### Before (In-Memory)
```python
# Data stored in a Python dictionary
db = {1: {"id": 1, "name": "Product", "price": 99.99}}

# Data lost when server restarts
```

### After (SQLite)
```python
# Data stored in SQLite database file
# Database persists on disk
# Can survive server restarts
```

---

## 📋 New Files

### 1. `db_init.py` - Database Initialization Script
**Purpose:** Creates the database and inserts seed data

**When to run:**
- First time setup (REQUIRED)
- When you want to reset data
- When database gets corrupted

**How to run:**
```bash
python db_init.py
```

### 2. `database.py` - Database Utility Module
**Purpose:** Contains all database operations

**Functions:**
- `get_all_items()` - Fetch all items
- `get_item_by_id(id)` - Fetch one item
- `create_item(name, price)` - Add new item
- `update_item(id, name, price)` - Update item
- `delete_item(id)` - Delete item
- `get_item_count()` - Count items

### 3. `main.py` - Updated FastAPI App
**Changes:**
- Uses `database.py` instead of dictionary
- Checks if database exists on startup
- Better error handling

### 4. `products.db` - SQLite Database File
**Created by:** `db_init.py`
**Contains:** All product data
**Location:** Same folder as Python files

---

## 🚀 Step-by-Step Setup

### Step 1: Install Dependencies (Same as before)
```bash
pip install -r requirements.txt
```

**Note:** No new dependencies needed! SQLite3 is built into Python.

### Step 2: Initialize Database (NEW STEP!)

```bash
python db_init.py
```

**What happens:**
1. Creates `products.db` file
2. Creates `items` table
3. Inserts 50 seed products
4. Verifies data was inserted

**Expected output:**
```
============================================================
DATABASE INITIALIZATION
============================================================

🔧 Creating database...
   ✅ Database created: products.db
   ✅ Table 'items' created

📦 Inserting seed data...
   ✅ Inserted 50 items

🔍 Verifying data...
   ✅ Total items in database: 50

   📋 Sample items:
      ID: 1, Name: Mechanical Keyboard, Price: $120.00
      ID: 2, Name: Wireless Mouse, Price: $45.50
      ID: 3, Name: UltraWide Monitor, Price: $350.00
      ID: 4, Name: USB-C Hub, Price: $25.99
      ID: 5, Name: Noise Cancelling Headphones, Price: $199.00

============================================================
✅ DATABASE INITIALIZATION COMPLETE!
============================================================
```

### Step 3: Start Server (Same as before)

```bash
uvicorn main:app --reload
```

**Or use the all-in-one script:**

Windows:
```bash
setup_and_start.bat
```

Mac/Linux:
```bash
./setup_and_start.sh
```

### Step 4: Verify Database Connection

Open http://localhost:8000 in your browser.

**Before (in-memory):**
```json
{"status": "API is running", "total_items": 50}
```

**After (SQLite):**
```json
{
  "status": "API is running",
  "database": "connected",
  "total_items": 50
}
```

---

## 🔧 Database Operations

### View All Data

**Option 1: Via API**
```bash
# Browser
http://localhost:8000/items/

# Or curl
curl http://localhost:8000/items/
```

**Option 2: Direct SQL (if sqlite3 is installed)**
```bash
sqlite3 products.db "SELECT * FROM items LIMIT 10;"
```

**Option 3: Python Script**
```python
import database as db

items = db.get_all_items()
for item in items[:5]:
    print(f"ID: {item['id']}, Name: {item['name']}, Price: ${item['price']}")
```

### Reset Database

```bash
python db_init.py
```

It will ask: `Do you want to recreate the database? (all data will be lost)`
- Type `y` to reset
- Type `n` to cancel

### Backup Database

**Windows:**
```bash
copy products.db products_backup.db
```

**Mac/Linux:**
```bash
cp products.db products_backup.db
```

### Restore from Backup

```bash
# Delete current database
rm products.db  # Mac/Linux
del products.db  # Windows

# Restore from backup
cp products_backup.db products.db  # Mac/Linux
copy products_backup.db products.db  # Windows
```

---

## 📊 Database Schema

```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Columns:**
- `id` - Auto-incrementing primary key
- `name` - Product name (required)
- `price` - Product price (required)
- `created_at` - Timestamp when item was created

---

## 🧪 Testing Database Performance

### Before Database Integration
- All data in memory (fast but not realistic)
- No disk I/O
- No database overhead

### After Database Integration
- Real database queries
- Disk I/O operations
- Connection management
- More realistic performance testing

### Run Load Tests

```bash
# Light load (test database reads)
locust -f locustfile.py --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 60s --headless

# Heavy load (stress test database)
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 300s --headless
```

**What to monitor:**
- Response times (should be <100ms for most requests)
- Database file size
- Disk I/O usage
- CPU usage

---

## 🐛 Troubleshooting

### Error: "Database not found"

**Problem:** You didn't run `db_init.py`

**Solution:**
```bash
python db_init.py
```

### Error: "no such table: items"

**Problem:** Database exists but table wasn't created

**Solution:**
```bash
# Delete corrupted database
rm products.db  # Mac/Linux
del products.db  # Windows

# Recreate
python db_init.py
```

### Database shows 0 items

**Problem:** Seed data wasn't inserted

**Solution:**
```bash
python db_init.py
# Choose 'y' to recreate
```

### "OperationalError: database is locked"

**Problem:** Multiple processes accessing database

**Solution:**
- Close any other programs accessing `products.db`
- Restart the FastAPI server
- SQLite doesn't handle high concurrency well (consider PostgreSQL for production)

### Changes not persisting

**Problem:** You might have multiple database files

**Solution:**
```bash
# Check current directory
ls -la *.db  # Mac/Linux
dir *.db  # Windows

# Should only see products.db
```

---

## 🚀 Advanced Usage

### Custom Database Queries

Edit `database.py` to add custom functions:

```python
def search_items_by_name(search_term: str) -> List[Dict[str, Any]]:
    """Search items by name"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, price FROM items WHERE name LIKE ? ORDER BY id",
            (f"%{search_term}%",)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
```

Then use in `main.py`:

```python
@app.get("/items/search/{term}")
def search_items(term: str):
    """Search items by name"""
    return db.search_items_by_name(term)
```

### Add Database Indexes

For better performance on large datasets:

```python
# In db_init.py, after creating the table
cursor.execute("CREATE INDEX idx_name ON items(name)")
cursor.execute("CREATE INDEX idx_price ON items(price)")
```

### Migrate to PostgreSQL

Ready for production? Upgrade to PostgreSQL:

1. Install PostgreSQL
2. Install psycopg2: `pip install psycopg2-binary`
3. Replace SQLite connection with PostgreSQL
4. Use SQLAlchemy ORM for easier migration

---

## 📚 Learning Resources

### SQLite
- Official docs: https://www.sqlite.org/docs.html
- Tutorial: https://www.sqlitetutorial.net/

### FastAPI + Databases
- FastAPI SQL Databases: https://fastapi.tiangolo.com/tutorial/sql-databases/
- SQLAlchemy: https://www.sqlalchemy.org/

### Database Tools
- DB Browser for SQLite: https://sqlitebrowser.org/
- DBeaver: https://dbeaver.io/

---

## ✅ Checklist

- [ ] Ran `python db_init.py` successfully
- [ ] See `products.db` file in project folder
- [ ] Server starts without "database not found" error
- [ ] http://localhost:8000 shows "database": "connected"
- [ ] Can view items at http://localhost:8000/items/
- [ ] Load tests run successfully
- [ ] Understand how to reset database
- [ ] Know how to backup database

---

**Questions?** Check the main README.md for more information!
