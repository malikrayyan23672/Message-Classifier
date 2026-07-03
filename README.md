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
GENAI_API_KEY=your_google_genai_api_key
```

3. Use `input_data.csv` as your source data, or pass a custom path.

## Usage
```bash
python main.py input_data.csv --output classified_output.csv
```

If you use a `.env` file, `python-dotenv` will load it automatically.

## Output
The script writes `message` and `category` columns to the specified output file.

## Notes
- The script uses the `gemini-3.5-flash` model.
- Categories are normalized to `Enrollment`, `Support`, or `General`.
- Invalid model responses default to `General`.

