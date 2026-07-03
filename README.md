# Internship Assessment Task

## Project Overview
This project reads incoming messages from a CSV file and classifies each one into a category:
- `Enrollment`
- `Support`
- `General`

The improved tool is now command-line friendly, avoids hard-coded API keys, and saves the categorized results to a new CSV file.

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
```bash
python main.py input_data.csv --output classified_output.csv

## Output
The script writes `message` and `category` columns to the specified output file.

## Notes
- The script uses the `gpt-4.1` model.
- Categories are normalized to `Enrollment`, `Support`, or `General`.
- Invalid model responses default to `General`.

