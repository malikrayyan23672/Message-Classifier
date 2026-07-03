from flask import Flask, redirect, render_template, request, url_for
import csv
import os

from main import append_classification_result, classify_message, create_client, get_api_key, DEFAULT_API_KEY_ENV

app = Flask(__name__)

api_key = get_api_key(DEFAULT_API_KEY_ENV)
if not api_key:
    raise RuntimeError(
        f"Missing API key. Set {DEFAULT_API_KEY_ENV} in your environment or .env file."
    )

client = create_client(api_key)
OUTPUT_FILE = "classified_output.csv"

def load_classification_results(filename):
    rows = []
    if not os.path.exists(filename):
        return rows
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i == 0 and row[:2] == ["message", "category"]:
                # Skip header row written by append_classification_result
                continue
            if row and len(row) >= 2:
                rows.append((row[0].strip(), row[1].strip()))
    return rows

@app.route("/", methods=["GET"])
def hello():
    app.logger.info("Loading classification results from %s", OUTPUT_FILE)
    items = load_classification_results(OUTPUT_FILE)
    return render_template("base.html", items=items)

@app.route("/classify", methods=["POST"])
def classify():
    message = (request.form.get("message") or "").strip()
    if message:
        try:
            classification = classify_message(client, message)
        except Exception as exc:
            app.logger.error("Failed to classify message: %s", exc)
            classification = "Error"

        append_classification_result(OUTPUT_FILE, message, classification)
        app.logger.info("Message: %s", message)
        app.logger.info("Category: %s", classification)

    return redirect(url_for("hello"))


if __name__ == "__main__":
    app.run(debug=True)