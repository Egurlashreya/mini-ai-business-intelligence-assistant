# Mini AI Business Intelligence Assistant

## Project Overview

The Mini AI Business Intelligence Assistant is a Python-based application that allows users to ask natural-language questions about sales data and receive structured business insights.

The application uses Google Gemini to understand the user's question and identify the required analytical operation. All numerical calculations are performed deterministically using Python and SQL to ensure reliable results.

## Features

The application supports the following business questions:

1. What is the total revenue?
2. Which product generated the highest revenue?
3. What is the monthly sales trend?
4. Which region has the highest sales?
5. Compare sales between two months.

Additional features:
- Natural-language question interpretation using Google Gemini.
- SQLite database for storing sales transactions.
- Deterministic SQL-based analytics.
- Input validation and unsupported-question handling.
- Streamlit user interface.
- Automated API tests using Pytest.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Database | SQLite |
| AI Model | Google Gemini |
| Data Processing | Pandas |
| Frontend | Streamlit |
| API Testing | Pytest |

## Project Structure

```text
mini-ai-business-intelligence-assistant/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── analytics.py
│   ├── main.py
│   └── ai_service.py
│
├── frontend/
│   └── streamlit_app.py
│
├── tests/
│   └── test_api.py
│
├── ai_bi_assistant_sales_data - GET.csv
├── requirements.txt
├── .gitignore
├── README.md
├── ARCHITECTURE.md
└── AI_DEVELOPMENT_NOTES.md
```

The SQLite database is generated locally during initialization and is not committed to the repository.

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd mini-ai-business-intelligence-assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash
```

Replace the placeholder with your own API key.

**Security:** Never commit the `.env` file or expose your API key publicly.

### 5. Initialize the database

Run this command from the project root:

```bash
python3 -c "from app.database import initialize_database; initialize_database()"
```

This initializes the SQLite database using the supplied CSV dataset.

## Running the Application

### Start the FastAPI backend

Open a terminal in the project root and run:

```bash
uvicorn app.main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Start the Streamlit frontend

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run frontend/streamlit_app.py
```

The Streamlit interface will open in your browser.

## Example Questions

Try asking:

- What is the total revenue?
- Which product generated the highest revenue?
- Show me the monthly sales trend.
- Which region has the highest sales?
- Compare sales between May 2026 and June 2026.

## Testing

The project includes automated API tests using Pytest.

Run the tests:

```bash
python3 -m pytest tests/ -v
```

The implemented test suite contains seven tests covering:

- Total revenue calculation.
- Top product identification.
- Highest sales region.
- Monthly sales trend.
- Unsupported questions.
- Empty questions.
- Month-to-month comparison.

**Latest recorded test result:** 7 tests passed.

## AI and Analytics Approach

The application separates language understanding from numerical computation.

1. The user submits a natural-language question.
2. Google Gemini interprets the question and identifies the appropriate analytical intent.
3. The backend validates the interpreted intent and required parameters.
4. Python and SQL execute the corresponding deterministic calculation.
5. The API returns a structured response containing the answer and supporting data.
6. The Streamlit frontend displays the result.

The AI model is used for question interpretation, not for calculating revenue or generating unrestricted SQL queries.

## Data Handling

The application stores the supplied sales transactions in SQLite.

Revenue is calculated using:

```text
Net Revenue = (Quantity × Unit Price) - Discount Amount
```

Returned and invalid transactions are excluded from revenue calculations. Source records are retained in the database with validation information.

## Limitations and Future Improvements

- Currently supports five predefined analytical question types.
- Natural-language interpretation depends on Gemini API availability.
- More business metrics and flexible date filters can be added.
- Authentication and deployment can be introduced for production use.
- Additional tests can cover more unusual user questions and data conditions.

## Author

Developed as part of the RSG Graduate Engineer Trainee assessment.

**Project:** Mini AI Business Intelligence Assistant
