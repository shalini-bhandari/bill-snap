
import asyncio
from pathlib import Path

from google import genai
from google.genai import types

from app.config import settings


async def main():
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    image_path = Path.home() / "Downloads" / "test-bill.jpeg"

    if not image_path.exists():
        print("Image not found:", image_path)
        return

    image_bytes = image_path.read_bytes()

    print("Testing model:", settings.GEMINI_MODEL)

    response = await client.aio.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=[
            "Analyze this image. Is it a bill or receipt? "
            "If yes, identify the merchant and final total amount.",
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
        ]
    )

    print("\nGemini image analysis:")
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
