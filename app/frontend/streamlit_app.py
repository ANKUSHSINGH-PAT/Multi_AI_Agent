import streamlit as st
from io import BytesIO

from app.backend.xaml_parser import parse_xaml
from app.backend.rules import detect_errors
from app.backend.llm_explainer import explain
from app.backend.pdf_report import generate_pdf

st.set_page_config(
    page_title="ICA Copilot - XAML Analyzer",
    layout="wide"
)

st.title("🤖 ICA Copilot - UiPath XAML Analyzer")

st.markdown("Upload your **Main.xaml** file to generate analysis report.")

uploaded_file = st.file_uploader(
    "Upload Main.xaml",
    type=["xaml"]
)

if uploaded_file is not None:
    try:
        content = uploaded_file.read()

        # Parse XAML
        tree, activities = parse_xaml(content)

        # Detect Errors
        errors, warnings = detect_errors(tree)

        # LLM Explanation
        try:
            llm_summary = explain(activities, errors, warnings)
        except Exception as llm_error:
            llm_summary = f"LLM failed: {llm_error}"

        st.success("Analysis Completed ✅")

        # Layout
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📌 Activities")
            st.json(activities)

        with col2:
            st.subheader("⚠ Errors")
            st.json(errors)

            st.subheader("⚠ Warnings")
            st.json(warnings)

        st.subheader("🤖 LLM Explanation")
        st.write(llm_summary)

        # Generate PDF
        pdf_buffer = generate_pdf(
            activities,
            errors,
            warnings,
            llm_summary
        )

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_buffer,
            file_name="ica_report.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"Error: {e}")