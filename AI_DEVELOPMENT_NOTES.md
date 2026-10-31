# AI Development Notes – Mini AI Business Intelligence Assistant

## 1. Objective

The objective of this project is to build a Mini AI Business Intelligence Assistant that allows users to ask questions about sales data in natural language and receive meaningful, structured business insights.

The application combines AI-based question interpretation with deterministic Python and SQL analytics.

## 2. Role of AI in the Application

Google Gemini is used as a natural-language interpretation component.

Its responsibilities include:

- Understanding the user's business question.
- Identifying the required analytical intent.
- Extracting month parameters for comparison questions.
- Returning structured JSON information to the backend.

The AI model is not responsible for calculating revenue, identifying the top product, or executing database queries.

These operations are handled by the analytics layer using Python and SQL.

## 3. AI Development Approach

The implementation follows these steps:

1. Defined the supported business questions.
2. Designed a prompt that instructs Gemini to classify questions into predefined analytical intents.
3. Restricted the expected output to structured JSON.
4. Parsed the AI response in the backend.
5. Validated the returned intent and required parameters.
6. Routed valid requests to deterministic analytics functions.
7. Returned the result through the FastAPI endpoint.

## 4. Supported Analytical Intents

| Intent | Description |
|---|---|
| total_revenue | Calculates total net revenue |
| top_product | Identifies the product with the highest revenue |
| monthly_trend | Returns revenue by month |
| top_region | Identifies the highest-revenue region |
| compare_months | Compares revenue between two months |
| unsupported | Handles questions outside the supported scope |

## 5. Why Use AI for Interpretation and SQL for Calculations?

Language models can understand different ways of expressing the same question, but their numerical outputs should not be treated as authoritative business calculations.

For example, users may ask:

- What is our total revenue?
- How much money did we generate?
- Calculate the overall sales revenue.

These questions can represent the same analytical intent.

Gemini interprets the question, while SQL and Python calculate the actual result from the database.

This separation improves reliability, consistency, and explainability.

## 6. Prompt Design

The AI prompt defines:

- The assistant's role.
- The available analytical intents.
- The expected JSON structure.
- The month extraction requirements.
- The instruction to return an unsupported intent for unrelated questions.

The backend validates the AI-generated response before using it.

## 7. Error Handling

The application considers the following cases:

- Empty questions.
- Unsupported questions.
- Missing month parameters.
- Invalid month formats.
- Gemini API failures.
- Database and analytics errors.

These checks help prevent invalid requests from reaching the analytics layer.

## 8. Testing and Validation

The project includes automated API tests using Pytest.

The test suite covers:

1. Total revenue calculation.
2. Top product identification.
3. Highest-sales region.
4. Monthly revenue trend.
5. Unsupported questions.
6. Empty questions.
7. Month-to-month comparison.

The recorded test result was **7 passed**.

The Gemini interpretation service was also tested separately with representative questions for the supported intents.

## 9. AI Limit
