# System Architecture – Mini AI Business Intelligence Assistant

## 1. Overview

The Mini AI Business Intelligence Assistant follows a simple layered architecture. It separates natural-language understanding, business logic, database operations, and user interaction.

The system uses Google Gemini to interpret questions, while Python and SQL perform the actual business calculations.

## 2. Architecture Diagram

```text
             USER
               |
               v
       STREAMLIT FRONTEND
               |
               v
         FASTAPI BACKEND
               |
               v
       GEMINI AI SERVICE
      (Question Interpretation)
               |
               v
       INTENT VALIDATION
               |
               v
       ANALYTICS MODULE
        (Python + SQL)
               |
               v
         SQLITE DATABASE
               |
               v
       STRUCTURED RESPONSE
               |
               v
       STREAMLIT FRONTEND
               |
               v
             USER
```

## 3. Main Components

### 3.1 Data Layer – database.py

Responsibilities:
- Loads the supplied CSV dataset.
- Initializes the SQLite database.
- Stores sales transaction records.
- Handles database connections.
- Maintains validation information for source records.

### 3.2 Analytics Layer – analytics.py

Responsibilities:
- Calculates total revenue.
- Identifies the highest-revenue product.
- Generates monthly revenue trends.
- Identifies the highest-sales region.
- Compares revenue between two months.

All numerical calculations are performed using deterministic Python and SQL operations.

### 3.3 AI Service Layer – ai_service.py

Responsibilities:
- Receives natural-language questions.
- Uses Google Gemini to understand the question.
- Identifies the analytical intent.
- Extracts month parameters when required.
- Returns structured intent information.

The AI service does not calculate business metrics or generate unrestricted SQL queries.

### 3.4 API Layer – main.py

Responsibilities:
- Exposes the `/ask` endpoint.
- Receives user questions.
- Calls the AI interpretation service.
- Validates the returned intent and parameters.
- Invokes the appropriate analytics function.
- Returns structured JSON responses.
- Handles invalid inputs and service errors.

### 3.5 Presentation Layer – streamlit_app.py

Responsibilities:
- Provides a simple interactive interface.
- Accepts natural-language questions.
- Sends requests to the FastAPI backend.
- Displays answers and supporting data.

## 4. Request Processing Flow

1. The user enters a business question in the Streamlit interface.
2. Streamlit sends the question to the FastAPI `/ask` endpoint.
3. The backend passes the question to the Gemini AI service.
4. Gemini identifies the question's intent and extracts required parameters.
5. The backend validates the interpreted intent and parameters.
6. The analytics module executes the corresponding SQL/Python calculation.
7. The result is converted into a structured JSON response.
8. Streamlit displays the answer and supporting information.

## 5. Database Design

The application uses SQLite to store the supplied sales transaction dataset.

The main table is:

**sales_transactions**

It contains the transaction information, including:

- Transaction ID
- Order date
- Product
- Category
- Region
- Sales channel
- Quantity
- Unit price
- Discount amount
- Transaction status
- Validation information
- Net revenue

The original source records are retained, while returned and invalid records are excluded from revenue calculations.

## 6. API Design

**Endpoint:** `POST /ask`

**Purpose:** Accepts a natural-language business question and returns an analytical result.

Example request:

```json
{
  "question": "What is the total revenue?"
}
```

Example response:

```json
{
  "question_type": "total_revenue",
  "answer": "Total revenue is ₹1,439,200.00",
  "supporting_data": {
    "total_revenue": 1439200.0,
    "transactions": 48,
    "units_sold": 633
  }
}
```

## 7. Error Handling and Validation

The application handles:
- Empty user questions.
- Unsupported analytical questions.
- Invalid month parameters.
- AI service failures.
- Database or analytics errors.

The system validates AI-interpreted intents before executing analytics operations.

## 8. Security and Reliability

- The Gemini API key is stored in an environment variable.
- The `.env` file is excluded from Git.
- Numerical calculations are performed deterministically.
- AI output is validated before routing.
- The application does not execute arbitrary AI-generated SQL.

## 9. Design Benefits

- Separation of concerns.
- Easier maintenance and testing.
- Reliable numerical calculations.
- Flexible natural-language interaction.
- Clear separation between AI interpretation and business logic.

## 10. Future Enhancements

- Support additional analytical questions.
- Add interactive charts and dashboards.
- Introduce authentication and authorization.
- Improve query interpretation and parameter extraction.
- Deploy the application to a cloud platform.
