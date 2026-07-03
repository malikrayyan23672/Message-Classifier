import argparse
import csv
import logging
import os
from typing import List, Tuple
from dotenv import load_dotenv, dotenv_values
from google import genai
from google.genai import types
from openai import OpenAI

from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

CATEGORIES = ["Enrollment", "Support", "General"]


def load_environment() -> None:
    load_dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    return dotenv_values(load_dotenv_path) if load_dotenv else None


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


def classify_message(client: genai.Client, message: str) -> str:


    response = client.chat.completions.create(
        model="openai/gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that classifies messages into one of three categories: Enrollment, Support, or General. Respond with only the single category name."},
            {"role": "user", "content": message},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    
    
    return response.choices[0].message.content


def write_classification_results(filename: str, rows: List[Tuple[str, str]]) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["message", "category"])
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify incoming messages into Enrollment, Support, or General."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="input_data.csv",
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="classified_output.csv",
        help="Path to the output CSV file.",
    )
    parser.add_argument(
        "--api-key-env",
        default="GENAI_API_KEY",
        help="Environment variable name for the Google GenAI API key.",
    )
    return parser.parse_args()

app = Flask(__name__)

def main() -> None:
    config = load_environment()
    args = parse_args()



    api_key = config.get("BAZARLINK_API_KEY")

    messages = read_messages_from_csv(args.csv_path)
    client = genai.Client(api_key=api_key)
    client = OpenAI(
    api_key=api_key,
    base_url="https://bazaarlink.ai/api/v1")

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
