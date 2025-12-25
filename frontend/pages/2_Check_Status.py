import streamlit as st
import requests
from config import API_BASE_URL

st.header("🔍 Check Project Status")

student_id = st.text_input(
    "Enter Student ID",
    placeholder="CSC-25F-123"
)

if st.button("Check Status", use_container_width=True):

    if not student_id:
        st.warning("⚠️ Please enter Student ID")
        st.stop()

    try:
        # Backend doesn't provide a direct "get-by-student-id" endpoint,
        # so fetch all submissions and filter locally.
        res = requests.get(f"{API_BASE_URL}/get-all-submissions")

        if res.status_code == 200:
            payload = res.json()
            submissions = payload.get("data", [])

            matches = []
            for sub in submissions:
                for m in sub.get("members", []):
                    if m.get("student_id") == student_id:
                        matches.append(sub)
                        break

            if not matches:
                st.error("❌ No submission found for that Student ID")
            else:
                # show first match (or you could iterate through all)
                data = matches[0]

                st.subheader("📄 Project Information")
                st.write("**Title:**", data["project_details"]["title"])
                st.write("**Description:**", data["project_details"]["description"])

                st.subheader("👥 Group Members")
                for m in data["members"]:
                    st.write(f"- {m.get('student_name','')} ({m.get('student_id')})")

                st.subheader("📊 Evaluation")
                st.metric("Status", data.get("status", "unknown"))
                st.metric("Marks", data.get("marks", 0))

        else:
            st.error("❌ Failed to fetch submissions from backend")

    except Exception:
        st.error("❌ Backend not reachable")
