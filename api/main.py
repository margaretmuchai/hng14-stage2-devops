from fastapi import FastAPI
import redis
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_password = os.getenv("REDIS_PASSWORD", None)

r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=False)

@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.rpush("jobs", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}

@app.get("/health")
def health_check():
    try:
        r.ping()
        return {"status": "ok", "redis": "connected"}
    except Exception as e:
        return {"status": "error", "redis": str(e)}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    return {"job_id": job_id, "status": status.decode() if isinstance(status, bytes) else status}
