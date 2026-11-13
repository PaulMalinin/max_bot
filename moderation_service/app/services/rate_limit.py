import redis.asyncio as redis
import os

from datetime import timedelta

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

redis_client = redis.Redis(host = redis_host, port = redis_port, db=0)

async def request_is_limited(r: redis.Redis, user_id: int, limit: int, period: timedelta):

    key = f"rate:{user_id}"

    period_in_seconds = int(period.total_seconds())
    t = (await r.time())[0]
    separation = max(round(period_in_seconds / limit), 1)
    await r.setnx(key, 0)
    tat = max(int(await r.get(key)), t)

    if tat - t <= period_in_seconds - separation:

        new_tat = max(tat, t) + separation
        await r.set(key, new_tat)

        return False
    
    return True