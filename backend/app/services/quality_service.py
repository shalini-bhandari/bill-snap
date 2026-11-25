import cv2
import numpy as np

BLUR_THRESHOLD = 100.0

def calculate_blur_score(image_bytes: bytes) -> float:
    """
        Calculate image sharpness using the variance of the Laplacian.
        Lower score = potentially more blurry.
        Higher score = potentially sharper.
    """

    image_array = np.frombuffer(image_bytes, dtype = np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Unable to read image for quality analysis.")

    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(grayscale, cv2.CV_64F)
    return float(laplacian.var())


def is_blurry(image_bytes: bytes) -> tuple[bool, float]:
    """
    Return whether an image is blurry and its blur score.
    """

    score = calculate_blur_score(image_bytes)
    return score < BLUR_THRESHOLD, score

def get_image_quality(image_bytes: bytes) -> dict[str, float | bool | str | None]:
    """
    Return image quality information without rejecting the image.
    """

    score = calculate_blur_score(image_bytes)

    return {
        "blur_score": round(score, 2),
        "is_blurry": score < BLUR_THRESHOLD,
        "quality_warning": (
            "This image may be blurry. "
            "You can still continue with analysis."
            if score < BLUR_THRESHOLD
            else None
        ),
    }