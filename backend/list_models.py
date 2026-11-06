
import asyncio
from google import genai
from app.config import settings


async def main():
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async for model in await client.aio.models.list():
        name = model.name or ""
        actions = model.supported_actions or []

        if "generateContent" in actions:
            print(name)


if __name__ == "__main__":
    asyncio.run(main())
