from PIL import Image, ImageFilter
from io import BytesIO

from app.services.quality_service import calculate_blur_score

image_path = "../evaluation/test_images/test-03.jpeg"

with Image.open(image_path) as image:
    original = image.convert("RGB")

    # Create increasingly blurred versions.
    for radius in [0, 1, 2, 4, 6]:
        blurred_image = original.filter(
            ImageFilter.GaussianBlur(radius=radius)
        )

        buffer = BytesIO()
        blurred_image.save(buffer, format="JPEG")

        score = calculate_blur_score(buffer.getvalue())

        print(f"Blur radius: {radius} | Score: {score:.2f}")