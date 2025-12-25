import streamlit as st
import requests
import json
from config import API_BASE_URL

st.header("📤 Submit Your Project")

st.subheader("👥Add Group Members")
member_count = st.number_input(
    "Number of group members",
    min_value=1,
    max_value=5,
    step=1
)

members = []
for i in range(member_count):
    with st.container():
        st.markdown(f"**Member {i+1}**")
        name = st.text_input("Student Name", key=f"name_{i}")
        sid = st.text_input("Student ID", key=f"id_{i}")

        if name and sid:
            members.append({
                "student_name": name,
                "student_id": sid
            })

st.subheader("📁 Project Details")
title = st.text_input("Project Title")
description = st.text_area("Project Description(Please Enter Full Description)")

uploaded_files = st.file_uploader(
    "Upload Project Files (ZIP recommended)",
    accept_multiple_files=True
)

st.markdown("---")

if st.button("🚀 Submit Project", use_container_width=True):

    if not members:
        st.error("Please add at least one group member")
        st.stop()

    if not title or not description:
        st.error("Please enter project title and description")
        st.stop()

    if not uploaded_files:
        st.error("Please upload at least one project file")
        st.stop()

    payload = {
        "members": members,
        "project_details": {
            "title": title,
            "description": description,
            "code_file_path": ""
        }
    }

    files = [
        ("files", (file.name, file.read(), file.type))
        for file in uploaded_files
    ]

    data = {
        "data": json.dumps(payload)
    }

    res = requests.post(
        f"{API_BASE_URL}/submit-project",
        data=data,
        files=files
    )

    if res.status_code == 200:
        st.success("✅ Project uploaded successfully!")
        st.balloons()
    else:
        st.error("❌ Submission failed")
        st.write("Status:", res.status_code)
        st.write("Response:", res.text)
