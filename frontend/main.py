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

st.markdown("---")

st.subheader("👨‍💻 Project Creators")

st.markdown("""
This **Project Submission System** has been designed and developed by:

- **Noman Haider** — *Student ID: CSC-25F-041*  
- **Zain Ul Abideen** — *Student ID: CSC-25F-008*

The application is developed as part of the **Programming Fundamentals Project** with a focus on clean architecture, scalability, and real-world backend integration.
""")

st.subheader("📌 Project Overview")

st.markdown("""
This system provides a complete workflow for **group-based project submissions**.  
Students can submit their project details and files through a user-friendly interface, while the backend ensures secure storage and structured data management.

### 🔧 Technology Stack & Architecture:
- **Frontend:** Streamlit (Python-based interactive UI)
- **Backend:** FastAPI (high-performance RESTful API)
- **Database:** MongoDB (NoSQL database for flexible data storage)
- **File Storage:** Google Drive (used to store uploaded project folders securely)

### 🚀 Key Functionalities:
- Group project submission with multiple members
- Upload complete project folders (code, description, code folder)
- Store project metadata in MongoDB
- Save project files to Google Drive and maintain reference links
- Retrieve submission status using Student ID
- Designed with API-based architecture for future scalability

This application demonstrates the practical use of **full-stack Python development**, integrating modern backend frameworks with cloud storage and database systems.
""")

st.markdown("---")