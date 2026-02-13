# ⚡ Quick Reference Card

## 🔥 Most Common Commands

### First Time Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database (REQUIRED!)
python db_init.py

# 3. Start server
uvicorn main:app --reload

# 4. In new terminal - Start load test
locust -f locustfile.py --host=http://localhost:8000
```

---

## 📊 Quick Load Tests

### Basic Test (10 users, 1 minute)
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 60s --headless
```

### Medium Test (50 users, 2 minutes)
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 120s --headless
```

### Stress Test (100 users, 5 minutes)
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 300s --headless
```

### Generate HTML Report
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 120s --headless --html report.html
```

---

## 🗄️ Database Commands

### Reset Database
```bash
python db_init.py
```

### Backup Database
```bash
# Windows
copy products.db products_backup.db

# Mac/Linux
cp products.db products_backup.db
```

### View Database (if sqlite3 installed)
```bash
sqlite3 products.db "SELECT * FROM items LIMIT 10;"
```

---

## 🔧 Helper Scripts

### All-in-One Setup and Start

**Windows:**
```bash
setup_and_start.bat
```

**Mac/Linux:**
```bash
./setup_and_start.sh
```

### Individual Scripts

**Start Server:**
```bash
start_server.bat        # Windows
./start_server.sh       # Mac/Linux
```

**Run Load Test:**
```bash
run_loadtest.bat        # Windows
./run_loadtest.sh       # Mac/Linux
```

---

## 🌐 URLs

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | API Health Check |
| http://localhost:8000/items/ | Get All Items |
| http://localhost:8000/items/1 | Get Item #1 |
| http://localhost:8000/docs | Interactive API Docs |
| http://localhost:8089 | Locust Web Interface |

---

## 🔍 Verify Setup

```bash
python verify_setup.py
```

---

## 🚨 Common Fixes

### Database Error
```bash
python db_init.py
```

### Port Already in Use
```bash
# Use different port
uvicorn main:app --port 8001
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Permission Denied (.sh files)
```bash
chmod +x *.sh
```

---

## 📈 What to Monitor

During load tests, watch for:
- ✅ Response time < 100ms (good)
- ⚠️ Response time 100-500ms (acceptable)
- 🚨 Response time > 500ms (slow)
- ✅ 0% failure rate (perfect)
- ⚠️ 1-5% failure rate (investigate)
- 🚨 >5% failure rate (serious issue)

---

## 💡 Pro Tips

1. **Always initialize database first!**
   ```bash
   python db_init.py
   ```

2. **Start small, then increase load**
   ```bash
   # Start with 5 users
   --users 5
   
   # Then 10, 20, 50, 100...
   ```

3. **Generate reports for documentation**
   ```bash
   --html report.html --csv results
   ```

4. **Monitor system resources**
   - Task Manager (Windows)
   - Activity Monitor (Mac)
   - htop (Linux)

5. **Backup before major tests**
   ```bash
   cp products.db backup.db
   ```

---

## 🎯 Typical Workflow

```bash
# Terminal 1
python db_init.py                    # First time only
uvicorn main:app --reload            # Start server

# Terminal 2
locust -f locustfile.py --host=http://localhost:8000
# Then open browser to http://localhost:8089
# Configure: 10 users, spawn rate 2
# Click "Start swarming"
# Watch the metrics!
```

---

## 📞 Need Help?

| Issue | Check |
|-------|-------|
| Database errors | README.md → Database Management |
| Server won't start | INSTALLATION_GUIDE.md → Troubleshooting |
| Load test fails | README.md → Troubleshooting |
| Understanding results | README.md → Understanding the Results |
| Database setup | DATABASE_SETUP_GUIDE.md |

---

**Print this page for quick reference while testing!**
