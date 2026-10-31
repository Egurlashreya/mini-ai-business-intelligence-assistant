
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Sales BI Assistant",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Mini AI Business Intelligence Assistant")
st.write("Ask questions about your sales data using natural language.")

st.info(
    "Try asking about total revenue, top product, "
    "monthly trends, highest-sales region, or comparing months."
)

question = st.text_input(
    "Enter your question",
    placeholder="What is the total revenue?"
)

if st.button("Get Answer", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Analyzing your sales data..."):
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=60
                )

            if response.status_code == 200:
                result = response.json()

                st.success("Analysis completed!")

                st.subheader("Your Answer")
                st.write(result.get("answer", "No answer available."))

                st.subheader("Supporting Data")
                st.json(result.get("supporting_data", {}))

                st.caption(
                    f"Question type: {result.get('question_type', 'Unknown')}"
                )

            else:
                st.error(f"API Error: {response.status_code}")
                st.write(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the backend. "
                "Please start the FastAPI server first."
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
