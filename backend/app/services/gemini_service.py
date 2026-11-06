import asyncio
from google import genai
from google.genai import types, errors
from app.config import settings
from app.schemas.bill import BillAnalysis

client = genai.Client(api_key=settings.GEMINI_API_KEY)

BILL_ANALYSIS_PROMPT = """
You are an AI assistant that analyzes images for a bill-scanning application.

Examine the uploaded image carefully.

1. Determine whether the image is an actual bill, receipt, or invoice.
2. If it is not a bill, set is_bill to false and set all bill-specific
   fields to null.
3. If it is a bill, extract:
   - Merchant or business name
   - Bill date in YYYY-MM-DD format
   - Final total amount payable
   - One category: Food, Utilities, or Groceries

IMPORTANT RULES:

- Do not invent missing information.
- If a field is unreadable or unavailable, return null.
- Extract the final amount payable, not the subtotal or tax.
- Do not confuse the transaction date with other dates.
- Food: restaurants, cafes, takeaway and food services.
- Utilities: electricity, water, gas, internet and similar bills.
- Groceries: supermarkets and grocery stores.
- If uncertain about the category, choose the closest category.
- Provide confidence scores between 0 and 1 for each field.
- Confidence scores are estimates, not guaranteed probabilities.
"""



async def analyze_image_with_gemini(
    image_bytes: bytes,
    mime_type: str
) -> BillAnalysis:

    # Retry temporary Gemini server failures
    for attempt in range(3):
        try:
            response = await client.aio.models.generate_content(
                model=settings.GEMINI_MODEL,

                contents=[
                    BILL_ANALYSIS_PROMPT,
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=mime_type
                    )
                ],

                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=BillAnalysis,
                    temperature=0.1
                )
            )

            break

        except errors.ServerError as error:
            if error.code != 503 or attempt == 2:
                raise

            delay = 2 ** attempt
            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {delay} seconds..."
            )

            await asyncio.sleep(delay)

    if response.parsed is not None:
        return BillAnalysis.model_validate(response.parsed)

    if response.text:
        return BillAnalysis.model_validate_json(response.text)

    raise ValueError("Gemini returned an empty response.")