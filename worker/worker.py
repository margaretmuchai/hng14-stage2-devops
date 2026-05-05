import redis
import time
import os
import signal

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_password = os.getenv("REDIS_PASSWORD", None)

r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=False)

running = True


def signal_handler(sig, frame):
    global running
    print(f"Received signal {sig}, shutting down gracefully...")
    running = False


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def process_job(job_id):
    try:
        print(f"Processing job {job_id}")
        time.sleep(2)
        r.hset(f"job:{job_id}", "status", "completed")
        print(f"Done: {job_id}")
    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        r.hset(f"job:{job_id}", "status", "failed")


while running:
    try:
        job = r.brpop("jobs", timeout=5)
        if job:
            _, job_id = job
            process_job(job_id.decode() if isinstance(job_id, bytes) else job_id)
    except Exception as e:
        print(f"Error fetching job: {e}")
        time.sleep(1)