import logging
import io

from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from datetime import timedelta
from PIL import Image

from app.services.rate_limit import request_is_limited, redis_client

app = FastAPI(title = "Moderation service", version = "0.1.0")

logger = logging.getLogger(__name__)

RATE_LIMIT = 5
RATE_PERIOD = timedelta(minutes=1)

MAX_SIZE = 15*1024*1024 # максимальный размер в байтах

@app.get("/health")
async def check_health():
    return {"status": "ok"}

@app.post("/moderate")
async def moderate_image(file: UploadFile = File(...), user_id: int | None = Header(None, alias="X-User-Id")):

    if user_id is None:
        raise HTTPException(status_code = 400, detail="'user_id' is not specified.")

    if await request_is_limited(redis_client, user_id, RATE_LIMIT, RATE_PERIOD):
        raise HTTPException(status_code=429, detail="The limit has been reached.")

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="The file is empty.")

    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=413, detail=f"The file size is too large. The maximum file size is {MAX_SIZE // (1024 * 1024)} MB.")
    try:
        image = Image.open(io.BytesIO(content))
        image.load()
    except Image.UnidentifiedImageError:
        raise HTTPException(status_code=415, detail="The uploaded file is not a valid image.")
    except OSError:
        raise HTTPException(status_code=400, detail="The image file appears to be corrupted or truncated.")
    except Exception as e:
        logger.exception("Unknown error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error.")


    return {
        "filename": file.filename or "unknown",
        "format": image.format,
        "width": image.width,
        "height": image.height,
        "bytes": len(content)
    }