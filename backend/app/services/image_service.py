from io import BytesIO
from PIL import Image, ImageOps, UnidentifiedImageError

MAX_IMAGE_DIMENSION = 2000
OUTPUT_FORMAT = "JPEG"

def preprocess_image(image_bytes: bytes) -> tuple[bytes, str]:
    """
    Normalize an uploaded bill image before sending it to Gemini.
    Returns:
        A tuple containing the processed image bytes and MIME type.
    """

    try:
        with Image.open(BytesIO(image_bytes)) as image:

            # Correct orientation using EXIF metadata.
            image = ImageOps.exif_transpose(image)

            # Convert to RGB because JPEG does not support transparency.
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Resize only when the image exceeds our maximum dimensions.
            image.thumbnail(
                (MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION),
                Image.Resampling.LANCZOS
            )

            # Save the processed image in memory.
            output = BytesIO()

            image.save(
                output,
                format=OUTPUT_FORMAT,
                quality=90,
                optimize=True
            )

            return output.getvalue(), "image/jpeg"

    except (UnidentifiedImageError, OSError, ValueError) as error:
        raise ValueError("Unable to process the uploaded image.") from error
