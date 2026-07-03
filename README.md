# Internship Assessment Task

## Project Overview
This project reads incoming messages from a CSV file and classifies each one into a category:
- `Enrollment`
- `Support`
- `General`

The improved tool is now command-line friendly, avoids hard-coded API keys, and saves the categorized results to a new CSV file.

## Approach
The solution uses a lightweight LLM-based classifier because it can understand natural language more flexibly than a rigid rule-based system. This makes it better suited for real customer messages, which often vary in phrasing, tone, and detail. The app keeps the output consistent by normalizing predictions into a small set of predefined categories and falling back to `General` when the model response is unclear.

## Setup
1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file or export the API key in your environment:

```env
BAZARLINK_API_KEY=YOUR BAZAR LINK API
```

3. Use `input_data.csv` as your source data, or pass a custom path.

## Usage

### Run the classifier from the command line
```bash
python main.py input_data.csv --output classified_output.csv
```

This writes `message` and `category` columns to the specified output file.

### Run the web app
```bash
python app.py
```

You can also start it with Flask directly:
```bash
flask --app app run
```

## Notes
- The script uses the `openai/gpt-4.1` model.
- Categories are normalized to `Enrollment`, `Support`, or `General`.
- Invalid model responses default to `General`.

