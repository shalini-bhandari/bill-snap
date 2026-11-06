import logging
from io import BytesIO

from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image, UnidentifiedImageError

from app.services.gemini_service import analyze_image_with_gemini

router = APIRouter(prefix="/api/bills", tags=["Bills"])
logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_FORMATS = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
}


@router.post("/analyze")
async def analyze_bill(file: UploadFile = File(...)):

    #1. Check content type
    if file.content_type not in ALLOWED_FORMATS.values():
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPEG, PNG, or WEBP image."
        )

    #2. Read uploaded file
    image_bytes = await file.read()

    #3. Check file size
    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image size must not exceed 10 MB."
        )

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    #4. Validate actual image content using Pillow
    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image_format = image.format

            if image_format not in ALLOWED_FORMATS:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported image format."
                )

            image.verify()

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image."
        )

    mime_type = ALLOWED_FORMATS[image_format]

    # 5. Send image to Gemini
    try:
        result = await analyze_image_with_gemini(
            image_bytes=image_bytes,
            mime_type=mime_type
        )

    except Exception:
        logger.exception("Gemini bill analysis failed")

        raise HTTPException(
            status_code=502,
            detail="Unable to analyze the image right now. Please try again."
        )

    return result.model_dump()

