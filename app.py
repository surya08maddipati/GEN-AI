import streamlit as st
import os

from resume_processor import (
    load_resume,
    analyze_resume,
    store_to_vectorstore,
    run_self_query,
    split_documents
)

# ================= UI =================
st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("AI Resume Screener")
st.markdown("Analyze resumes and perform intelligent search using Gemini AI")

# ================= INPUT =================
job_desc = st.text_area("📌 Paste Job Description")

uploaded_file = st.file_uploader(
    "📂 Upload Resume",
    type=["pdf", "docx", "txt"]
)

# ================= ANALYZE =================
if st.button("Analyze & Store"):
    if not uploaded_file or not job_desc:
        st.warning("⚠️ Please provide both resume and job description")
    else:
        os.makedirs("temp", exist_ok=True)
        file_path = os.path.join("temp", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Processing..."):
            docs = load_resume(file_path)

            # ✅ FIX: Split documents properly
            chunks = split_documents(docs)

            # ✅ Analyze using chunks
            report = analyze_resume(chunks, job_desc)

            # ✅ Store chunks (not raw docs)
            store_to_vectorstore(chunks)

        st.success("✅ Resume analyzed and stored successfully!")

        st.subheader("📄 AI Analysis")
        st.write(report)

        st.download_button(
            "📥 Download Report",
            report,
            file_name="resume_analysis.txt"
        )

st.divider()

# ================= SEARCH =================
st.subheader("🔍 Smart Resume Search")

query = st.text_input("Enter query (e.g., Python developer with AWS)")

if st.button("Search"):
    if not query:
        st.warning("⚠️ Please enter a query")
    else:
        with st.spinner("Searching..."):
            results = run_self_query(query)

        if results:
            for i, res in enumerate(results, 1):
                st.markdown(f"### Result {i}")
                st.write(res.page_content)
        else:
            st.warning("No results found")