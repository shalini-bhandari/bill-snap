
import asyncio
from pathlib import Path

from app.services.gemini_service import analyze_image_with_gemini


async def main():
    image_path = Path.home() / "Downloads" / "test-nonbill.jpg"

    if not image_path.exists():
        print("Image not found:", image_path)
        return

    image_bytes = image_path.read_bytes()

    try:
        result = await analyze_image_with_gemini(
            image_bytes=image_bytes,
            mime_type="image/jpg"
        )

        print("\nStructured Gemini response:")
        print(result.model_dump_json(indent=2))

    except Exception as error:
        print("Structured extraction failed:")
        print(type(error).__name__)
        print(error)


if __name__ == "__main__":
    asyncio.run(main())
