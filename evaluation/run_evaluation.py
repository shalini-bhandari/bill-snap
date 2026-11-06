
import csv
import time
import requests
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "test_images"
GROUND_TRUTH = BASE_DIR / "ground_truth.csv"
RESULTS_FILE = BASE_DIR / "results.csv"

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/api/bills/analyze"

# Rate-limit settings
DELAY_BETWEEN_REQUESTS = 15
MAX_RETRIES = 4


def analyze_image(image_path):
    """Send an image to the backend, retrying temporary API failures."""

    for attempt in range(MAX_RETRIES):
        try:
            with open(image_path, "rb") as image:
                files = {
                    "file": (
                        image_path.name,
                        image,
                        "image/jpeg"
                    )
                }

                response = requests.post(
                    API_URL,
                    files=files,
                    timeout=180
                )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            print(f"Request failed: {error}")

            if attempt < MAX_RETRIES - 1:
                wait_time = 15 * (2 ** attempt)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Maximum retries reached.")
                return None

    return None


def save_results(results):
    """Save progress immediately to the results CSV."""

    if not results:
        return

    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)


def main():

    # Load ground truth
    with open(GROUND_TRUTH, "r", newline="", encoding="utf-8") as file:
        ground_truth = list(csv.DictReader(file))

    # Load previous results if available
    existing_results = {}

    if RESULTS_FILE.exists():
        with open(RESULTS_FILE, "r", newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                existing_results[row["image_name"]] = row

    results = []

    for index, sample in enumerate(ground_truth, start=1):

        image_name = sample["image_name"]
        image_path = IMAGE_DIR / image_name

        print(f"\n[{index}/{len(ground_truth)}] Testing: {image_name}")

        # Reuse previously successful predictions
        previous = existing_results.get(image_name)

        if previous and previous.get("predicted_is_bill", "") != "":
            print("Already evaluated successfully. Skipping.")

            results.append(previous)
            continue

        if not image_path.exists():
            print("Image not found. Skipping.")
            continue

        # Wait before making another API request
        print(f"Waiting {DELAY_BETWEEN_REQUESTS} seconds...")
        time.sleep(DELAY_BETWEEN_REQUESTS)

        prediction = analyze_image(image_path)

        if prediction is None:
            prediction = {}

        result = {
            "image_name": image_name,
            "actual_is_bill": sample["is_bill"],
            "predicted_is_bill": prediction.get("is_bill", ""),
            "actual_merchant": sample["merchant_name"],
            "predicted_merchant": prediction.get("merchant_name", ""),
            "actual_date": sample["bill_date"],
            "predicted_date": prediction.get("bill_date", ""),
            "actual_amount": sample["total_amount"],
            "predicted_amount": prediction.get("total_amount", ""),
            "actual_category": sample["category"],
            "predicted_category": prediction.get("category", ""),
            "confidence": prediction.get("confidence", ""),
        }

        results.append(result)

        # Save after every image
        save_results(results)

        print("Prediction:", prediction)

        if prediction:
            print("Result saved.")
        else:
            print("No prediction received. This image can be retried later.")

    print("\nEvaluation completed!")
    print(f"Results saved to: {RESULTS_FILE}")
    print(f"Images with saved rows: {len(results)}/{len(ground_truth)}")


if __name__ == "__main__":
    main()
