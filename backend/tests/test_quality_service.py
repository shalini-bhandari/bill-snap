from io import BytesIO

import cv2
import numpy as np

from app.services.quality_service import (
    calculate_blur_score,
    is_blurry,
    get_image_quality
)


def create_test_image(blur=False):
    # Create a high-detail checkerboard image.
    image = np.zeros((300, 300), dtype=np.uint8)
    image[::10, :] = 255
    image[:, ::10] = 255

    if blur:
        image = cv2.GaussianBlur(image, (31, 31), 0)

    success, encoded = cv2.imencode(".jpg", image)
    assert success
    return encoded.tobytes()


def test_sharp_image_has_higher_blur_score():
    sharp_image = create_test_image()
    blurry_image = create_test_image(blur=True)

    sharp_score = calculate_blur_score(sharp_image)
    blurry_score = calculate_blur_score(blurry_image)

    assert sharp_score > blurry_score


def test_blurry_image_is_detected():
    blurry_image = create_test_image(blur=True)
    blurry, score = is_blurry(blurry_image)

    assert blurry is True
    assert score < 100.0


def test_sharp_image_is_not_detected_as_blurry():
    sharp_image = create_test_image()
    blurry, score = is_blurry(sharp_image)

    assert blurry is False
    assert score >= 100.0

def test_clear_image_has_no_quality_warning():
    sharp_image = create_test_image()

    result = get_image_quality(sharp_image)

    assert result["is_blurry"] is False
    assert result["quality_warning"] is None
    assert isinstance(result["blur_score"], float)


def test_blurry_image_returns_warning():
    blurry_image = create_test_image(blur=True)

    result = get_image_quality(blurry_image)

    assert result["is_blurry"] is True
    assert result["quality_warning"] is not None
    assert result["blur_score"] < 100.0