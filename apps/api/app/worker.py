import os
import time

from app.queue import QUEUE_NAME


def main() -> None:
    url = os.getenv("REDIS_URL")
    if not url:
        while True:
            time.sleep(10)
        return

    import redis

    client = redis.Redis.from_url(url)
    while True:
        try:
            item = client.brpop(QUEUE_NAME, timeout=5)
        except Exception:
            time.sleep(2)
            continue
        if item is None:
            continue


if __name__ == "__main__":
    main()
