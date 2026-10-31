
# app/analytics.py

def total_revenue(conn):
    query = """
        SELECT
            SUM(net_revenue) AS total_revenue,
            COUNT(*) AS transaction_count,
            SUM(Quantity) AS total_units
        FROM sales_transactions
        WHERE validation_status = 'VALID'
    """

    result = conn.execute(query).fetchone()

    return {
        "question_type": "total_revenue",
        "answer": f"Total revenue is ₹{result[0]:,.2f}",
        "supporting_data": {
            "total_revenue": result[0],
            "transactions": result[1],
            "units_sold": result[2]
        }
    }


def top_product(conn):
    query = """
        SELECT Product, SUM(net_revenue) AS revenue
        FROM sales_transactions
        WHERE validation_status = 'VALID'
        GROUP BY Product
        ORDER BY revenue DESC
        LIMIT 1
    """

    result = conn.execute(query).fetchone()

    return {
        "question_type": "top_product",
        "answer": f"{result[0]} generated the highest revenue of ₹{result[1]:,.2f}",
        "supporting_data": {
            "product": result[0],
            "revenue": result[1]
        }
    }


def monthly_trend(conn):
    query = """
        SELECT
            strftime('%Y-%m', Order_date) AS month,
            SUM(net_revenue) AS revenue
        FROM sales_transactions
        WHERE validation_status = 'VALID'
        GROUP BY strftime('%Y-%m', Order_date)
        ORDER BY month
    """

    rows = conn.execute(query).fetchall()

    data = [
        {"month": row[0], "revenue": row[1]}
        for row in rows
    ]

    return {
        "question_type": "monthly_trend",
        "answer": "Monthly revenue trend retrieved successfully.",
        "supporting_data": data
    }


def top_region(conn):
    query = """
        SELECT Region, SUM(net_revenue) AS revenue
        FROM sales_transactions
        WHERE validation_status = 'VALID'
        GROUP BY Region
        ORDER BY revenue DESC
        LIMIT 1
    """

    result = conn.execute(query).fetchone()

    return {
        "question_type": "top_region",
        "answer": f"{result[0]} generated the highest sales of ₹{result[1]:,.2f}",
        "supporting_data": {
            "region": result[0],
            "revenue": result[1]
        }
    }


def compare_months(conn, month1, month2):

    query = """
        SELECT
            strftime('%Y-%m', Order_date) AS month,
            SUM(net_revenue) AS revenue
        FROM sales_transactions
        WHERE validation_status = 'VALID'
          AND strftime('%Y-%m', Order_date) IN (?, ?)
        GROUP BY strftime('%Y-%m', Order_date)
    """

    rows = conn.execute(query, (month1, month2)).fetchall()

    revenue = {row[0]: row[1] for row in rows}

    value1 = revenue.get(month1, 0)
    value2 = revenue.get(month2, 0)

    difference = value2 - value1

    percentage = (
        (difference / value1) * 100
        if value1 != 0 else None
    )

    if difference > 0:
        direction = "increased"
    elif difference < 0:
        direction = "decreased"
    else:
        direction = "remained unchanged"

    return {
        "question_type": "compare_months",
        "answer": f"Revenue {direction} by ₹{abs(difference):,.2f}",
        "supporting_data": {
            "month1": month1,
            "revenue1": value1,
            "month2": month2,
            "revenue2": value2,
            "difference": difference,
            "percentage_change": percentage
        }
    }
