from io import BytesIO
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app
from app.schemas.bill import BillAnalysis, FieldConfidence
from app.config import settings
from unittest.mock import AsyncMock, patch
from slowapi.errors import RateLimitExceeded

settings.BETA_ACCESS_CODE = "test-beta-code"
client = TestClient(app)
TEST_HEADERS = {
    "X-Beta-Code": "test-beta-code"
}

def create_test_image():
    image = Image.new("RGB", (800, 600), color="white")
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_analyze_bill_returns_image_quality():
    mock_result = BillAnalysis(
        is_bill=True,
        merchant_name="Test Restaurant",
        bill_date="2026-11-25",
        total_amount=450.0,
        category="Food",
        confidence=FieldConfidence(
            is_bill =0.99,
            merchant_name=0.95,
            bill_date=0.98,
            total_amount=0.97,
            category=0.96
        )
    )

    with patch(
        "app.routes.bills.analyze_image_with_gemini",
        new_callable=AsyncMock,
        return_value=mock_result
    ):
        response = client.post(
            "/api/bills/analyze",
            files={
                "file": (
                    "receipt.jpg",
                    create_test_image(),
                    "image/jpeg"
                )
            },
            headers=TEST_HEADERS
        )

    assert response.status_code == 200

    data = response.json()

    assert data["is_bill"] is True
    assert data["merchant_name"] == "Test Restaurant"
    assert data["bill_date"] == "2026-11-25"
    assert data["confidence"]["is_bill"] == 0.99
    assert "image_quality" in data
    assert "blur_score" in data["image_quality"]
    assert "is_blurry" in data["image_quality"]
    assert "quality_warning" in data["image_quality"]

def test_rejects_unsupported_file_type():
    response = client.post(
        "/api/bills/analyze",
        files={
            "file": (
                "document.txt",
                b"Hello, this is not an image.",
                "text/plain"
            )
        },
        headers=TEST_HEADERS
    )

    assert response.status_code == 400


def test_rejects_invalid_image_content():
    response = client.post(
        "/api/bills/analyze",
        files={
            "file": (
                "fake.jpg",
                b"This is not a valid JPEG image.",
                "image/jpeg"
            )
        },
        headers=TEST_HEADERS
    )

    assert response.status_code == 400

def test_rejects_missing_beta_code():
    response = client.post(
        "/api/bills/analyze",
        files={
            "file": (
                "receipt.jpg",
                create_test_image(),
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Invalid or missing beta access code."
    )


def test_rejects_invalid_beta_code():
    response = client.post(
        "/api/bills/analyze",
        files={
            "file": (
                "receipt.jpg",
                create_test_image(),
                "image/jpeg"
            )
        },
        headers={"X-Beta-Code": "wrong-code"}
    )

    assert response.status_code == 401

def test_rate_limit_blocks_sixth_request():
    mock_result = BillAnalysis(
        is_bill=True,
        merchant_name="Test Restaurant",
        bill_date="2026-11-25",
        total_amount=450.0,
        category="Food",
        confidence=FieldConfidence(
            is_bill=0.99,
            merchant_name=0.95,
            bill_date=0.98,
            total_amount=0.97,
            category=0.96
        )
    )

    with patch(
        "app.routes.bills.analyze_image_with_gemini",
        new_callable=AsyncMock,
        return_value=mock_result
    ) as mock_gemini:
        test_client = TestClient(
            app,
            client=("192.0.2.10", 50000)
        )

        responses = []

        for _ in range(6):
            response = test_client.post(
                "/api/bills/analyze",
                files={
                    "file": (
                        "receipt.jpg",
                        create_test_image(),
                        "image/jpeg"
                    )
                },
                headers=TEST_HEADERS
            )
            responses.append(response.status_code)

    assert responses == [200, 200, 200, 200, 200, 429]
    assert mock_gemini.await_count == 5
