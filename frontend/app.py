import streamlit as st

st.set_page_config(
    page_title="Project Submission System",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Project Submission Application")

st.markdown("""
Welcome to the **Project Submission Portal (Programming Fundamental Project)**.

### Features:
- 📤 Submit group projects
- 🔍 Check project status using Student ID
- 📊 Transparent evaluation system

Use the **sidebar** to navigate.
""")
st.info("📌 Note: One submission per group. All members share the same status & marks.")
