# ⚡ QUICK START GUIDE

## 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 2️⃣ Initialize Database

**IMPORTANT: Run this FIRST before starting the server!**

```bash
python db_init.py
```

This creates `products.db` with 50 seeded items.

## 3️⃣ Start the API Server

**Windows:**
```bash
setup_and_start.bat
```
OR manually:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Mac/Linux:**
```bash
./setup_and_start.sh
```
OR manually:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ Verify: Open http://localhost:8000 in your browser

## 4️⃣ Run Load Test (in a NEW terminal)

**Windows:**
```bash
run_loadtest.bat
```

**Mac/Linux:**
```bash
./run_loadtest.sh
```

**OR manually:**
```bash
locust -f locustfile.py --host=http://localhost:8000
```

## 5️⃣ Configure Test in Browser

1. Go to: http://localhost:8089
2. Enter number of users: `10`
3. Enter spawn rate: `2`
4. Click "Start swarming"

## 🎯 That's It!

Watch the real-time statistics and charts in your browser.

---

## 📊 Quick CLI Test (No Browser)

```bash
locust -f locustfile.py --host=http://localhost:8000 --users 20 --spawn-rate 4 --run-time 60s --headless
```

This runs a 60-second test with 20 users in your terminal.

---

## 🔄 Reset Database

To reset the database with fresh seed data:

```bash
python db_init.py
```

It will ask if you want to recreate the database.

---

## ❓ Need Help?

See `README.md` for detailed documentation and troubleshooting.
