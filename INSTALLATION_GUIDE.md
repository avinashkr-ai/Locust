# 🚀 FastAPI Load Testing - Complete Installation Guide

## 📦 What You've Downloaded

You have a complete load testing setup with:
- **FastAPI Application** (main.py) - REST API with 50 seeded products
- **Load Testing Script** (locustfile.py) - Simulates realistic user behavior
- **Helper Scripts** - One-click server and test runners
- **Documentation** - README, Quick Start, and configuration examples

---

## ⚡ Installation Steps

### Step 1: Extract Files

Download all files to a folder on your computer, for example:
- Windows: `C:\Users\YourName\fastapi-load-test`
- Mac/Linux: `~/fastapi-load-test`

### Step 2: Open Terminal/Command Prompt

**Windows:**
- Press `Win + R`
- Type `cmd` and press Enter
- Navigate to your folder: `cd C:\Users\YourName\fastapi-load-test`

**Mac:**
- Press `Cmd + Space`
- Type `terminal` and press Enter
- Navigate to your folder: `cd ~/fastapi-load-test`

**Linux:**
- Open your terminal
- Navigate to your folder: `cd ~/fastapi-load-test`

### Step 3: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Your terminal should now show `(venv)` at the beginning.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install (takes about 1-2 minutes).

### Step 5: Initialize Database

**⚠️ IMPORTANT: This step is REQUIRED before starting the server!**

```bash
python db_init.py
```

You should see:
```
========================================
DATABASE INITIALIZATION
========================================

🔧 Creating database...
   ✅ Database created: products.db
   ✅ Table 'items' created

📦 Inserting seed data...
   ✅ Inserted 50 items

🔍 Verifying data...
   ✅ Total items in database: 50
```

This creates a file called `products.db` with 50 products.

### Step 6: Verify Installation

```bash
python verify_setup.py
```

You should see all green checkmarks ✅

---

## 🎯 Running the Load Test

### Option 1: Using All-in-One Script (Easiest)

**Windows:**
```bash
setup_and_start.bat
```

This will:
1. Check if database exists (create if needed)
2. Start the FastAPI server automatically

**Mac/Linux:**
```bash
./setup_and_start.sh
```

Then in a **NEW terminal**, run the load test:

Windows:
```bash
run_loadtest.bat
```

Mac/Linux:
```bash
./run_loadtest.sh
```

### Option 2: Step-by-Step (Manual Control)

**Terminal 1 - Start the API Server:**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Run Load Test:**

Open a NEW terminal window, navigate to the same folder, and activate the virtual environment again. Then:

```bash
locust -f locustfile.py --host=http://localhost:8000
```

Your browser will open to http://localhost:8089

### Option 3: Command Line Only (No Browser)

**Terminal 1 - Start Server:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Run Headless Test:**
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 20 --spawn-rate 4 --run-time 60s --headless
```

---

## 🎮 Using the Locust Web UI

Once you open http://localhost:8089:

1. **Number of users**: How many simulated users (start with 10)
2. **Spawn rate**: Users added per second (start with 2)
3. Click **"Start swarming"**

You'll see:
- Total requests per second
- Response times (50th, 95th, 99th percentile)
- Number of failures
- Real-time charts

To stop: Click **"Stop"** button

---

## 📊 What the Load Test Does

The test simulates realistic user behavior:

| Action | Weight | What it does |
|--------|--------|--------------|
| View Product | 50% | GET /items/{id} - User views specific product |
| Browse Catalog | 25% | GET /items/ - User browses all products |
| Add Product | 12.5% | POST /items/ - User adds new product |
| 404 Test | 12.5% | Tests error handling |

Wait time between actions: 0.5-2 seconds (realistic user thinking time)

---

## 🔍 Understanding the Results

### Good Performance Indicators
- ✅ Response time < 100ms for 95% of requests
- ✅ 0% failure rate
- ✅ Steady requests per second

### Warning Signs
- ⚠️ Response time > 500ms
- ⚠️ Increasing failures
- ⚠️ Response time growing as users increase

### Action Required
- 🚨 Response time > 1000ms
- 🚨 Failure rate > 5%
- 🚨 Server crashes or errors

---

## 🛠️ Testing Different Scenarios

See `load_test_configs.txt` for pre-configured test commands.

**Quick Tests:**
```bash
# 5 users, 30 seconds
locust -f locustfile.py --host=http://localhost:8000 --users 5 --spawn-rate 1 --run-time 30s --headless

# 20 users, 2 minutes
locust -f locustfile.py --host=http://localhost:8000 --users 20 --spawn-rate 4 --run-time 120s --headless
```

**Stress Tests:**
```bash
# 100 users
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 300s --headless

# Generate HTML report
locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 120s --headless --html report.html
```

---

## ❓ Troubleshooting

### "Command not found: uvicorn" or "Command not found: locust"
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

### "Address already in use"
- Port 8000 is occupied
- Kill the process or use different port: `uvicorn main:app --port 8001`

### Connection refused during load test
- Make sure FastAPI server is running in another terminal
- Check the URL is correct: `http://localhost:8000`

### High failure rate
- Too many users for your machine
- Reduce users: try 10-20 instead of 100+

### Permission denied on .sh files (Mac/Linux)
```bash
chmod +x start_server.sh run_loadtest.sh setup_and_start.sh
```

### "Database not found" error
- You forgot to run `python db_init.py`
- Run it now, then restart the server

### "Table not found" error
- Database was corrupted or incomplete
- Delete `products.db` file
- Run `python db_init.py` again

### Database shows 0 items
- Seed data wasn't inserted properly
- Run `python db_init.py` and choose to recreate

### Want to reset all data
```bash
python db_init.py
```
Choose "Y" when asked to recreate the database

---

## 📁 File Overview

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application (the API being tested, uses SQLite) |
| `database.py` | Database utility functions for SQLite operations |
| `db_init.py` | **Initialize database - RUN THIS FIRST!** |
| `locustfile.py` | Load testing script (simulates users) |
| `requirements.txt` | Python dependencies |
| `README.md` | Detailed documentation |
| `QUICKSTART.md` | Quick start guide |
| `verify_setup.py` | Check if everything is installed |
| `setup_and_start.bat/.sh` | All-in-one setup and start script |
| `start_server.bat/.sh` | Start API server only |
| `run_loadtest.bat/.sh` | Start load test (Windows/Mac/Linux) |
| `load_test_configs.txt` | Example test commands |
| `.gitignore` | Git ignore file (if using version control) |
| `products.db` | SQLite database (created by db_init.py) |

---

## 🎓 Learning Path

1. **Start Small**: Run with 5 users to understand the UI
2. **Increase Load**: Try 10, 20, 50, 100 users
3. **Find Limits**: Keep increasing until you see performance degrade
4. **Analyze**: Look at response times, failures, and charts
5. **Optimize**: Make improvements to your API
6. **Re-test**: Verify improvements work

---

## 🌐 Accessing the API

While the server is running:

- **Health Check**: http://localhost:8000
- **All Items**: http://localhost:8000/items/
- **Specific Item**: http://localhost:8000/items/1
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

---

## 📈 Next Steps

1. **Understand baseline**: Run with 10 users to see normal performance
2. **Test limits**: Gradually increase users (20, 50, 100, 200)
3. **Generate reports**: Use `--html report.html` flag
4. **Modify tests**: Edit `locustfile.py` to test different scenarios
5. **Improve API**: Add caching, database, optimize queries
6. **Re-test**: Compare performance before/after changes

---

## 💡 Pro Tips

- **Monitor System Resources**: Watch CPU/RAM usage during tests
- **Start Conservative**: Begin with low user counts
- **Use Headless Mode**: For automated testing in CI/CD
- **Save Reports**: Generate HTML reports for documentation
- **Test Incrementally**: Don't jump from 10 to 1000 users
- **Check Logs**: Monitor FastAPI terminal for errors

---

## 🆘 Need More Help?

1. Check `README.md` for detailed documentation
2. See `load_test_configs.txt` for more test examples
3. Visit Locust docs: https://docs.locust.io/
4. Visit FastAPI docs: https://fastapi.tiangolo.com/

---

## ✅ Quick Checklist

- [ ] Extracted all files to a folder
- [ ] Created virtual environment
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] **Initialized database (`python db_init.py`)** ⚠️ IMPORTANT
- [ ] Verified setup (`python verify_setup.py`)
- [ ] Started FastAPI server (Terminal 1)
- [ ] Started Locust (Terminal 2)
- [ ] Opened http://localhost:8089
- [ ] Ran first test with 10 users
- [ ] Checked results and charts

---

**Ready to Start?** Run these commands:

**First time setup:**
```bash
python db_init.py
```

**Then open two terminals:**

**Terminal 1:**
```bash
uvicorn main:app --reload
```

**Terminal 2:**
```bash
locust -f locustfile.py --host=http://localhost:8000
```

**Or use the all-in-one script:**

Windows: `setup_and_start.bat`
Mac/Linux: `./setup_and_start.sh`

Then visit: **http://localhost:8089** 🚀

Good luck with your load testing!
