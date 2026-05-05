# FIXES.md - Application Bug Fixes

## Issue 1: Redis Password Not Being Used
**File:** `api/main.py` (line 8), `worker/worker.py` (line 6)
**Problem:** The `.env` file contains `REDIS_PASSWORD=supersecretpassword123` but neither the API nor the Worker read it or use it for Redis authentication. Both connect without a password.
**Fix:** Read the password from environment variables and pass it to Redis connection.

---

## Issue 2: Job Queue Direction (FIFO vs LIFO)
**File:** `api/main.py` (line 13)
**Problem:** Jobs are added using `lpush` (adds to the head/front), but the worker uses `brpop` (waits and pops from the tail/back). This results in LIFO (Last In, First Out) behavior instead of FIFO.
**Fix:** Use `rpush` in the API to add jobs to the tail, and update worker to use `blpop` or keep using `brpop` with proper direction.

---

## Issue 3: Hardcoded Redis Host in API
**File:** `api/main.py` (line 8)
**Problem:** `redis.Redis(host="localhost", port=6379)` is hardcoded and won't work in containerized environments where services have different hostnames.
**Fix:** Use environment variables with fallback to localhost.

---

## Issue 4: Hardcoded Redis Host in Worker
**File:** `worker/worker.py` (line 6)
**Problem:** Same as Issue 3 - hardcoded localhost won't work in containers.
**Fix:** Use environment variables with fallback to localhost.

---

## Issue 5: Hardcoded API URL in Frontend
**File:** `frontend/app.js` (line 6)
**Problem:** `const API_URL = "http://localhost:8000";` is hardcoded and won't work in containers.
**Fix:** Use environment variable `process.env.API_URL` with fallback.

---

## Issue 6: Worker No Error Handling
**File:** `worker/worker.py` (lines 8-12)
**Problem:** The `process_job()` function has no try/except. Any error crashes the worker silently.
**Fix:** Wrap processing in try/except with proper error handling.

---

## Issue 7: No Graceful Shutdown in Worker
**File:** `worker/worker.py` (lines 14-17)
**Problem:** No signal handlers for SIGTERM/SIGINT. The worker won't gracefully shutdown when container stops.
**Fix:** Add signal handlers for graceful shutdown.

---

## Issue 8: Unpinned Dependencies in API requirements.txt
**File:** `api/requirements.txt`
**Problem:** Dependencies are not version-pinned (`fastapi`, `uvicorn`, `redis`). This can cause breakages when dependencies update.
**Fix:** Pin versions to known working versions.

---

## Issue 9: Unpinned Dependencies in Worker requirements.txt
**File:** `worker/requirements.txt`
**Problem:** `redis` dependency not version-pinned.
**Fix:** Pin redis version.

---

## Issue 10: .env File Tracked in Git
**File:** `api/.env`
**Problem:** The `.env` file containing secrets (`REDIS_PASSWORD`) is committed to git, exposing credentials.
**Fix:** Add to `.gitignore`.

---

## Issue 11: JavaScript Typo in HTML
**File:** `frontend/views/index.html` (line 41)
**Problem:** `getElementId` should be `getElementById`.
**Fix:** Fix the typo.

---

## Issue 12: Frontend Missing Error Handling
**File:** `frontend/views/index.html` (lines 23-28)
**Problem:** `submitJob()` doesn't check if `res.ok` before parsing JSON. Failed requests will throw errors.
**Fix:** Check response status before using data.