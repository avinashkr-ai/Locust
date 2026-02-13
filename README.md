# FastAPI Load Testing Setup

Complete setup for load testing a FastAPI application using Locust.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A terminal/command prompt

## 🚀 Quick Start

### Step 1: Create Project Directory

```bash
# Create a new directory for your project
mkdir fastapi-load-test
cd fastapi-load-test
```

### Step 2: Set Up Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

**⚠️ IMPORTANT: Run this BEFORE starting the server!**

```bash
python db_init.py
```

This will:
- Create `products.db` SQLite database
- Create the `items` table
- Insert 50 seed products
- Verify the data

You should see output like:
```
🔧 Creating database...
   ✅ Database created: products.db
   ✅ Table 'items' created

📦 Inserting seed data...
   ✅ Inserted 50 items

🔍 Verifying data...
   ✅ Total items in database: 50
```

### Step 5: Start the FastAPI Server

**Option A: Using helper script**

Windows:
```bash
setup_and_start.bat
```

Mac/Linux:
```bash
./setup_and_start.sh
```

**Option B: Manual start**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify the API is running:**
- Open your browser and go to: http://localhost:8000
- You should see: `{"status":"API is running","database":"connected","total_items":50}`
- API docs available at: http://localhost:8000/docs

### Step 6: Run Load Tests

Open a terminal and run:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify the API is running:**
- Open your browser and go to: http://localhost:8000
- You should see: `{"status":"API is running","total_items":50}`
- API docs available at: http://localhost:8000/docs

### Step 5: Run Load Tests

**Option A: Using Locust Web UI (Recommended for beginners)**

In a **NEW terminal** (keep the FastAPI server running), activate the virtual environment again and run:

```bash
locust -f locustfile.py --host=http://localhost:8000
```

Then:
1. Open your browser to: http://localhost:8089
2. Enter the number of users to simulate (e.g., 10)
3. Enter the spawn rate (users per second, e.g., 2)
4. Click "Start swarming"
5. Watch the real-time statistics, charts, and response times

**Option B: Headless Mode (Command Line)**

For automated testing without the web UI:

```bash
locust -f locustfile.py --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 60s --headless
```

This will:
- Simulate 10 concurrent users
- Spawn 2 users per second
- Run for 60 seconds
- Display results in the terminal

## 📊 Understanding the Load Test

### Task Weights

The load test simulates realistic user behavior with different operation frequencies:

- **GET /items/{id}** (Weight: 4) - 50% of requests
  - Most common: Users viewing specific products
  
- **GET /items/** (Weight: 2) - 25% of requests
  - Moderate: Browsing the full catalog
  
- **POST /items/** (Weight: 1) - 12.5% of requests
  - Less frequent: Adding new products
  
- **GET /items/{fake_id}** (Weight: 1) - 12.5% of requests
  - Testing 404 error handling

### Key Metrics to Monitor

1. **Requests per Second (RPS)** - Throughput capacity
2. **Response Time** - How fast your API responds
   - 50th percentile (median)
   - 95th percentile (most requests)
   - 99th percentile (slowest requests)
3. **Failure Rate** - Percentage of failed requests
4. **Number of Users** - Concurrent load

## 🔧 Customizing the Load Test

### Adjust User Behavior

Edit `locustfile.py`:

```python
# Change wait time between requests
wait_time = between(1, 3)  # Wait 1-3 seconds

# Modify task weights
@task(10)  # Increase weight to make this task more frequent
def test_get_item(self):
    ...
```

### Test Different Load Levels

**Light Load:**
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 5 --spawn-rate 1 --run-time 30s --headless
```

**Medium Load:**
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 120s --headless
```

**Heavy Load:**
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 200 --spawn-rate 10 --run-time 300s --headless
```

**Stress Test (Find breaking point):**
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 1000 --spawn-rate 50 --run-time 180s --headless
```

## 📁 Project Structure

```
fastapi-load-test/
│
├── main.py              # FastAPI application (uses SQLite)
├── database.py          # Database utility functions
├── db_init.py          # Database initialization script
├── locustfile.py        # Locust load testing script
├── requirements.txt     # Python dependencies
├── products.db         # SQLite database (created by db_init.py)
├── setup_and_start.bat # All-in-one setup script (Windows)
├── setup_and_start.sh  # All-in-one setup script (Mac/Linux)
└── README.md           # This file
```

## 🎯 Testing Workflow

1. **Baseline Test**: Run with 1-5 users to establish baseline performance
2. **Incremental Load**: Gradually increase users (10, 25, 50, 100)
3. **Identify Bottlenecks**: Note when response times start degrading
4. **Stress Test**: Push until failures occur to find breaking point
5. **Optimize**: Make code improvements
6. **Repeat**: Test again to verify improvements

## 📈 Sample Load Test Commands

### Quick Performance Check (30 seconds)
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 20 --spawn-rate 4 --run-time 30s --headless
```

### Standard Load Test (2 minutes)
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 120s --headless
```

### Extended Stress Test (5 minutes)
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 300s --headless
```

### Save Results to File
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 60s --headless --html report.html --csv results
```

This generates:
- `report.html` - Visual HTML report
- `results_stats.csv` - Statistics
- `results_failures.csv` - Failure details

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Make sure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: "Address already in use"
**Solution:** The port 8000 is already occupied. Either:
- Stop the other process using port 8000
- Use a different port: `uvicorn main:app --port 8001`

### Issue: Connection errors during load test
**Solution:** 
- Verify FastAPI server is running
- Check the host URL matches: `--host=http://localhost:8000`
- Ensure firewall isn't blocking connections

### Issue: High failure rate
**Solution:**
- Reduce number of users or spawn rate
- Check server logs for errors
- Your API might be hitting resource limits

## 🗄️ Database Management

### Reset Database

To reset the database with fresh seed data:

```bash
python db_init.py
```

The script will ask if you want to recreate the database (this will delete all existing data).

### View Database Contents

You can use any SQLite browser tool, or query directly:

```bash
# Using sqlite3 command line (if available)
sqlite3 products.db "SELECT * FROM items LIMIT 10;"
```

### Database Schema

The `items` table has the following structure:

```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Manual Database Operations

You can interact with the database programmatically:

```python
import database as db

# Get all items
items = db.get_all_items()

# Get specific item
item = db.get_item_by_id(1)

# Create new item
new_item = db.create_item("New Product", 99.99)

# Update item
updated = db.update_item(1, "Updated Name", 149.99)

# Delete item
deleted = db.delete_item(1)

# Get count
count = db.get_item_count()
```

### Backup Database

To backup your database:

```bash
# Windows
copy products.db products_backup.db

# Mac/Linux
cp products.db products_backup.db
```

## 🔍 Monitoring Tips

1. **Watch server CPU/Memory**: Use Task Manager (Windows) or Activity Monitor (Mac) to monitor resource usage
2. **Check terminal output**: Look for errors in the FastAPI server logs
3. **Use Locust charts**: The web UI provides real-time graphs
4. **Start small**: Begin with low user counts and increase gradually

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Locust Documentation](https://docs.locust.io/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

## 🎓 Next Steps

1. ~~Add database integration (PostgreSQL, MongoDB)~~ ✅ **SQLite already integrated!**
2. Add database indexes for better performance
3. Implement caching (Redis)
4. Add authentication/authorization testing
5. Test file upload endpoints
6. Measure API performance under different database loads
7. Migrate to PostgreSQL for production scenarios
8. Set up CI/CD pipeline with automated load tests
9. Add database connection pooling
10. Implement database migrations with Alembic

## 📝 Notes

- The SQLite database persists between server restarts
- All 50 seed items are loaded on database initialization
- Load tests simulate realistic user patterns with random delays
- Monitor your system resources during heavy load tests
- Database is stored in `products.db` file
- To reset data, run `python db_init.py` again
