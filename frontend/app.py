import streamlit as st
import requests


BACKEND_URL = "https://ai-financial-assistant-backend-th11.onrender.com"


st.set_page_config(
    page_title="AI Financial Assistant",
    page_icon="💹",
    layout="wide"
)


st.title("💹 AI Financial Assistant")
st.write(
    "Upload a financial PDF and ask questions using a RAG-powered assistant with citations."
)


# -----------------------------
# Sidebar: Upload PDF
# -----------------------------
st.sidebar.header("📄 Upload Financial Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    if st.sidebar.button("Process PDF"):
        with st.spinner("Uploading and processing PDF..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            try:
                response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files=files,
                    timeout=300
                )

                if response.status_code == 200:
                    st.sidebar.success("PDF processed successfully.")
                    st.sidebar.write(response.json())
                else:
                    st.sidebar.error("PDF processing failed.")
                    st.sidebar.write(response.text)

            except Exception as e:
                st.sidebar.error(f"Backend error: {e}")


# -----------------------------
# Main: Ask Questions
# -----------------------------
st.header("Ask Questions From Your Financial Document")

query = st.text_input(
    "Enter your question",
    placeholder="Example: What are the major risk factors mentioned in the report?"
)

if st.button("Ask Assistant"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving context and generating answer..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    data={"query": query},
                    timeout=300
                )

                if response.status_code == 200:
                    result = response.json()

                    st.subheader("Answer")
                    st.write(result["answer"])

                    st.subheader("Sources / Citations")

                    sources = result.get("sources", [])

                    if sources:
                        for source in sources:
                            with st.expander(
                                f"{source['citation']} - Page {source['page']}"
                            ):
                                st.write(source["text"])
                    else:
                        st.info("No sources returned.")

                else:
                    st.error("Failed to get answer.")
                    st.write(response.text)

            except Exception as e:
                st.error(f"Backend error: {e}")

st.sidebar.divider()

if st.sidebar.button("Clear Vector Database"):
    try:
        response = requests.delete(
            f"{BACKEND_URL}/reset"
        )

        if response.status_code == 200:
            st.sidebar.success(
                "Vector database cleared successfully."
            )
        else:
            st.sidebar.error(
                "Failed to clear vector database."
            )

    except Exception as e:
        st.sidebar.error(f"Backend error: {e}")
        
# -----------------------------
# Financial Sentiment Analysis
# -----------------------------
st.divider()

st.header("📊 Financial Sentiment Analysis")

sentiment_text = st.text_area(
    "Enter financial news, headline, or market statement",
    placeholder="Example: Apple reported strong revenue growth and improved margins this quarter."
)

if st.button("Analyze Sentiment"):
    if not sentiment_text.strip():
        st.warning("Please enter some financial text.")
    else:
        with st.spinner("Analyzing financial sentiment using FinBERT..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/sentiment",
                    data={"text": sentiment_text},
                    timeout=120
                )

                if response.status_code == 200:
                    result = response.json()

                    st.subheader("Sentiment Result")
                    st.write(f"**Sentiment:** {result['sentiment']}")
                    st.write(f"**Confidence:** {result['confidence']}")

                else:
                    st.error("Sentiment analysis failed.")
                    st.write(response.text)

            except Exception as e:
                st.error(f"Backend error: {e}")