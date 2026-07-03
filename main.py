import argparse
import csv
import logging
import os
import sys
from typing import List, Optional, Tuple

from dotenv import load_dotenv
from openai import OpenAI

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

CATEGORIES = ["Enrollment", "Support", "General"]
DEFAULT_INPUT_FILE = "input_data.csv"
DEFAULT_OUTPUT_FILE = "classified_output.csv"
DEFAULT_API_KEY_ENV = "BAZARLINK_API_KEY"


def load_environment() -> None:
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)


def get_api_key(env_name: str) -> Optional[str]:
    load_environment()
    return os.getenv(env_name)


def create_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, base_url="https://bazaarlink.ai/api/v1")


def read_messages_from_csv(filename: str) -> List[str]:
    try:
        with open(filename, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            messages = [row[0].strip() for row in reader if row and row[0].strip()]
    except FileNotFoundError as exc:
        logger.error("Input file not found: %s", filename)
        raise exc

    if not messages:
        raise ValueError(f"No messages found in '{filename}'.")

    return messages


def normalize_category(text: str) -> str:
    cleaned = text.strip().strip('"').strip()
    if not cleaned:
        return "General"
    candidate = cleaned.split()[0]
    for category in CATEGORIES:
        if candidate.lower() == category.lower():
            return category
    return "General"


def classify_message(client: OpenAI, message: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that classifies messages into one of three categories: "
                    "Enrollment, Support, or General. Respond with only the single category name."
                ),
            },
            {"role": "user", "content": message},
        ],
        max_tokens=1000,
        temperature=0.0,
        stream=False,
    )

    choice = response.choices[0]
    content = None
    if hasattr(choice, "message"):
        content = getattr(choice.message, "content", None)
    elif isinstance(choice, dict):
        content = choice.get("message", {}).get("content")

    if not content:
        raise ValueError("Model response did not contain classification text.")

    return normalize_category(content)


def write_classification_results(filename: str, rows: List[Tuple[str, str]]) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["message", "category"])
        writer.writerows(rows)


def append_classification_result(filename: str, message: str, category: str) -> None:
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["message", "category"])
        writer.writerow([message, category])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify incoming messages into Enrollment, Support, or General."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=DEFAULT_INPUT_FILE,
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=DEFAULT_OUTPUT_FILE,
        help="Path to the output CSV file.",
    )
    parser.add_argument(
        "--api-key-env",
        default=DEFAULT_API_KEY_ENV,
        help="Environment variable name for the API key.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api_key = get_api_key(args.api_key_env)
    if not api_key:
        logger.error(
            "Missing API key. Set %s in your environment or in a .env file.",
            args.api_key_env,
        )
        sys.exit(1)

    client = create_client(api_key)
    messages = read_messages_from_csv(args.csv_path)
    results: List[Tuple[str, str]] = []

    for message in messages:
        try:
            category = classify_message(client, message)
        except Exception as exc:
            logger.error("Failed to classify message: %s", exc)
            category = "Error"

        results.append((message, category))
        logger.info("Message: %s", message)
        logger.info("Category: %s", category)
        logger.info("%s", "-" * 40)

    write_classification_results(args.output, results)
    logger.info("Saved %d classified messages to %s", len(results), args.output)


if __name__ == "__main__":
    main()