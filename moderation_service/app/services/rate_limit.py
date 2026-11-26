import redis.asyncio as redis

from datetime import timedelta

async def request_is_limited(r: redis.Redis, user_id: int, limit: int, period: timedelta):

    key = f"rate:{user_id}"

    period_in_seconds = int(period.total_seconds())
    t = (await r.time())[0]
    separation = max(round(period_in_seconds / limit), 1)
    await r.setnx(key, 0) # set if not exists
    tat = max(int(await r.get(key)), t) # theoretical Arrival Time

    if tat - t <= period_in_seconds - separation:

        new_tat = max(tat, t) + separation
        await r.set(key, new_tat)

        return False
    
    return True