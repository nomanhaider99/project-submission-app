import os
import streamlit as st
import requests
import webbrowser
from config import API_BASE_URL

st.set_page_config(
    page_title="Admin Panel",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Admin Panel – Project Evaluation")

# --------------------------------------------------
# Simple Admin Authentication
# --------------------------------------------------
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"] 

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.subheader("🔐 Admin Login")
    password = st.text_input("Enter Admin Password", type="password")

    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.success("✅ Logged in successfully")
            st.rerun()  # <<< REQUIRED
        else:
            st.error("❌ Incorrect password")

    st.stop()


# --------------------------------------------------
# Fetch All Submissions
# --------------------------------------------------
try:
    response = requests.get(f"{API_BASE_URL}/get-all-submissions")
    submissions = response.json()["data"]
except Exception:
    st.error("❌ Unable to connect to backend")
    st.stop()

if not submissions:
    st.info("No submissions available yet.")
    st.stop()

# --------------------------------------------------
# Display Submissions
# --------------------------------------------------
for sub in submissions:

    with st.expander(f"📁 {sub['project_details']['title']}"):

        col1, col2 = st.columns(2)

        # -----------------------------
        # Left Column – Project Info
        # -----------------------------
        with col1:
            st.subheader("👥 Group Members")
            for member in sub["members"]:
                st.write(f"- {member['student_name']} ({member['student_id']})")

            st.subheader("📄 Project Description")
            st.write(sub["project_details"]["description"])

            drive_link = sub["project_details"]["code_file_path"]

            if drive_link:
                st.markdown("### 📁 Project Files")

                # Clickable link
                st.markdown(
                    f"🔗 **[Open Google Drive Folder]({drive_link})**",
                    unsafe_allow_html=True
                )

                # Copy-friendly text box
                st.text_input(
                    "Drive Folder Link",
                    value=drive_link,
                    disabled=True
                )

                # Optional button (opens browser)
                if st.button("📂 Open in Browser", key=f"open_{sub['_id']}"):
                    webbrowser.open_new_tab(drive_link)

        # -----------------------------
        # Right Column – Evaluation
        # -----------------------------
        with col2:
            st.subheader("📊 Evaluation")

            st.write("**Status:**", sub["status"])
            st.write("**Total Marks:**", sub["marks"])

            # Already evaluated
            if sub["status"] == "checked":
                st.success("✅ This project has already been evaluated.")
                continue

            st.markdown("### 🧪 Testing Marks (Out of 3)")

            testing_marks = st.number_input(
                "Enter testing marks",
                min_value=0.0,
                max_value=3.0,
                step=0.25,
                format="%.2f",
                key=sub["_id"]
            )

            if st.button("✅ Submit Evaluation", key=f"btn_{sub['_id']}"):

                if testing_marks < 0 or testing_marks > 3:
                    st.error("❌ Marks must be between 0 and 3")

                else:
                    res = requests.patch(
                        f"{API_BASE_URL}/update-marks/{sub['_id']}",
                        json={"marks": testing_marks}
                    )

                    if res.status_code == 200:
                        st.success("🎉 Evaluation submitted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to submit evaluation")
