from io import BytesIO

from PIL import Image

from app.services.image_service import preprocess_image


def create_test_image(size, image_format="JPEG"):
    image = Image.new("RGB", size, color="white")
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return buffer.getvalue()


def test_large_image_is_resized():
    image_bytes = create_test_image((3000, 2000))

    processed_bytes, mime_type = preprocess_image(image_bytes)

    processed_image = Image.open(BytesIO(processed_bytes))

    assert processed_image.size == (2000, 1333)
    assert mime_type == "image/jpeg"


def test_small_image_keeps_original_dimensions():
    image_bytes = create_test_image((800, 600))

    processed_bytes, mime_type = preprocess_image(image_bytes)

    processed_image = Image.open(BytesIO(processed_bytes))

    assert processed_image.size == (800, 600)
    assert mime_type == "image/jpeg"


def test_png_is_converted_to_jpeg():
    image_bytes = create_test_image((800, 600), "PNG")

    processed_bytes, mime_type = preprocess_image(image_bytes)

    processed_image = Image.open(BytesIO(processed_bytes))

    assert processed_image.format == "JPEG"
    assert mime_type == "image/jpeg"