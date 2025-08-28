import streamlit as st
import requests

st.set_page_config(page_title="📚 AI Document Assistant", page_icon="🤖")

backend_url = "http://localhost:8000"

st.title("📚 AI Document Assistant")

# Tabs for different features
tab1, tab2 ,tab3= st.tabs(["📄 RAG Q&A", "📝 Text Summarization" , "Dynamic Learning Path Suggestion"])

# ---------------- TAB 1: RAG Q&A ----------------
with tab1:
    st.header("📄 RAG Document Q&A")

    # Upload PDF for RAG
    pdf_file = st.file_uploader("Upload a PDF for Q&A", type=["pdf"], key="rag_pdf")
    if st.button("Upload PDF", key="rag_upload") and pdf_file:
        res = requests.post(
            f"{backend_url}/upload_pdf/",
            files={"file": ("doc.pdf", pdf_file, "application/pdf")}
        )
        if res.status_code == 200:
            st.success(res.json()["message"])
        else:
            st.error(res.text)

    # Ask question
    query = st.text_input("Enter your question:", key="rag_query")
    if st.button("Ask", key="rag_ask"):
        res = requests.post(f"{backend_url}/qa/", json={"query": query})
        if res.status_code == 200:
            data = res.json()
            st.subheader("Answer:")
            st.write(data["answer"])
            with st.expander("Context"):
                for c in data["context"]:
                    st.write(c)
        else:
            st.error(res.text)

# ---------------- TAB 2: Text Summarization ----------------
with tab2:
    st.header("📝 Text Summarization")

    option = st.radio("Choose input type:", ["Upload PDF", "Enter Text"])

    if option == "Upload PDF":
        pdf_sum = st.file_uploader("Upload a PDF for summarization", type=["pdf"], key="sum_pdf")
        if st.button("Summarize PDF"):
            if pdf_sum:
                res = requests.post(
                    f"{backend_url}/summarize/",
                    files={"file": ("doc.pdf", pdf_sum, "application/pdf")}
                )
                if res.status_code == 200:
                    st.success(res.json()["summary"])
                else:
                    st.error(res.text)
            else:
                st.error("Please upload a PDF")

    elif option == "Enter Text":
        text_input = st.text_area("Enter text to summarize", height=200)
        if st.button("Summarize Text"):
            if text_input.strip():
                res = requests.post(
                    f"{backend_url}/summarize/",
                    data={"text": text_input}
                )
                if res.status_code == 200:
                    data = res.json()
                    if "summary" in data:
                        st.subheader("Summary:")
                        st.write(data["summary"])
                    else:
                        st.error(data.get("error", "Unknown error"))
                else:
                    st.error(res.text)
            else:
                st.error("Please enter some text")

with tab3:
    st.header('Dynamic Learning Path Suggestion')

    goal = st.text_input("Enter your learning goal")
    current_skills = st.text_input("Enter your current skills (comma separated)")
    timeframe = st.text_input("Enter your timeframe")
    weekly_hours = st.text_input("Enter your weekly hours")

    if st.button("Generate Path"):
        res = requests.post(
            f"{backend_url}/learning-path/",
            json={   # 👈 use json not data
            'goal': goal,
            'current_skills': current_skills,
            'timeframe': timeframe,
            'weekly_hours': weekly_hours
            }
        )
        if res.status_code == 200:
            data = res.json()
            if "Learning Path" in data:
                st.subheader("📘 Suggested Learning Path")
                st.markdown(data["Learning Path"])
            else:
                st.error(data)
        else:
            st.error(res.text)
