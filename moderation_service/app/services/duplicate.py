import time
import imagehash
import redis.asyncio as redis

from PIL import Image

HAMMING_THRESHOLD = 5
DUBLICATE_WINDOW_SECONDS = 600
SAMPLE_LENGTH = 10
DUBLICATE_LIMIT = 3

def compute(image: Image.Image) -> str:
    hash = imagehash.phash(image)

    return str(hash)

async def check_dublicate(r: redis.Redis, user_id: int, new_hash: str) -> bool:
    key = f"phash:{user_id}"
    raw_entries = await r.lrange(key, 0, SAMPLE_LENGTH-1)

    new_hash_obj = imagehash.hex_to_hash(new_hash)
    now = int(time.time())
    cnt = 0
    for entry in raw_entries:
        entry_str = entry.decode()

        ts_str, old_hash = entry_str.split(":", 1)
        ts = int(ts_str)

        if now - ts > DUBLICATE_WINDOW_SECONDS:
            continue

        old_hash_obj = imagehash.hex_to_hash(old_hash)
        distance = new_hash_obj - old_hash_obj

        if distance <= HAMMING_THRESHOLD:
            cnt+=1
            if cnt >= DUBLICATE_LIMIT - 1:
                return True

    return False
    
    