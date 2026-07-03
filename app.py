from flask import Flask, render_template, request, jsonify
import csv
from main import classify_message

def load_classification_results(filename):
    rows = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and len(row) >= 2:
                rows.append((row[0].strip(), row[1].strip()))
    return rows

def load_data():
    # Load your data here (e.g., from a CSV file or database)
    # For demonstration, we'll use a static list of messages
    return [
        "I need help with my enrollment process.",
        "Can you assist me with technical support?",
        "What are the general guidelines for using this service?"
    ]

@app.route("/")
def hello():
    items = load_classification_results("classified_output.csv")
    return render_template("base.html", items=items)