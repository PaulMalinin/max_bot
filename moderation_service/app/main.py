from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import logging
import io

app = FastAPI(title = "Moderation service", version = "0.1.0")

logger = logging.getLogger(__name__)

MAX_SIZE = 15*1024*1024 # максимальный размер в байтах

@app.get("/health")
async def check_health():
    return {"status": "ok"}


@app.post("/moderate")
async def moderate_image(file: UploadFile = File(...)):
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