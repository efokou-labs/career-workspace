import json
import os

QUEUE_NAME = "applications:created"


def enqueue_created(company: str, role: str, status: str) -> None:
    url = os.getenv("REDIS_URL")
    if not url:
        return
    try:
        import redis

        client = redis.Redis.from_url(url)
        client.lpush(
            QUEUE_NAME,
            json.dumps({"company": company, "role": role, "status": status}),
        )
    except Exception:
        return
