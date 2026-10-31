from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from app.ai_service import interpret_question
from app.database import get_connection

from app.analytics import (
    total_revenue,
    top_product,
    monthly_trend,
    top_region,
    compare_months
)

app = FastAPI(
    title="Mini AI Business Intelligence Assistant",
    description="Ask natural-language questions about sales data.",
    version="1.0"
)


class QuestionRequest(BaseModel):
    question: str


def validate_month(month):
    if not isinstance(month, str):
        return False

    try:
        datetime.strptime(month, "%Y-%m")
        return True
    except ValueError:
        return False


@app.get("/")
def home():
    return {
        "message": "Mini AI Business Intelligence Assistant is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # Step 1: Ask Gemini to identify the question intent
    try:
        interpretation = interpret_question(question)
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"AI interpretation service unavailable: {str(e)}"
        )

    intent = interpretation["intent"]

    # Step 2: Reject unsupported questions
    if intent == "unsupported":
        return {
            "question": question,
            "answer": "Sorry, I can answer only supported sales analytics questions.",
            "question_type": "unsupported"
        }

    # Step 3: Execute the corresponding database analytics
    conn = get_connection()

    try:
        if intent == "total_revenue":
            result = total_revenue(conn)

        elif intent == "top_product":
            result = top_product(conn)

        elif intent == "monthly_trend":
            result = monthly_trend(conn)

        elif intent == "top_region":
            result = top_region(conn)

        elif intent == "compare_months":

            month1 = interpretation.get("month1")
            month2 = interpretation.get("month2")

            if not validate_month(month1) or not validate_month(month2):
                raise HTTPException(
                    status_code=400,
                    detail="Please provide two valid months in YYYY-MM format."
                )

            result = compare_months(conn, month1, month2)

        else:
            raise HTTPException(
                status_code=400,
                detail="Unknown question intent"
            )

        return {
            "question": question,
            **result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analytics error: {str(e)}"
        )

    finally:
        conn.close()