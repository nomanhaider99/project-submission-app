# from database import connect_to_database
# from models import Submission
# from datetime import datetime
# from fastapi import HTTPException
# from mailer import send_email_message
# from dotenv import load_dotenv
# import os
# from bson import ObjectId
# from pymongo import ReturnDocument
# from fastapi import UploadFile, File, Form
# from typing import List
# from drive import create_folder, upload_file_to_folder, get_folder_link
# import json, os, uuid, shutil


# load_dotenv()

# db = connect_to_database()
# submissions = db.get_collection("submissions")

# def submit_project(group_data: Submission):
#     try:
#         current_time = datetime.now()
#         deadline = datetime(2026, 1, 1)

#         if current_time < deadline:
#             group_data.marks += 5

#         result = submissions.insert_one(group_data.model_dump())

#         return {
#             "message": "Project Submitted Successfully!",
#             "id": str(result.inserted_id)
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# def get_submission_details(id: str):
#     try:
#         submission = submissions.find_one({ "_id": ObjectId(id) })

#         if not submission:
#             raise HTTPException(status_code=404, detail="Submission Not Found")

#         submission["_id"] = str(submission["_id"])

#         return {
#             "message": "Submission Retrieved Successfully!",
#             "data": submission
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# def get_all_submissions():
#     try:
#         submissions_list = list(submissions.find({}))

#         if not submissions_list:
#             raise HTTPException(status_code=404, detail="Submissions Not Found")

#         for sub in submissions_list:
#             sub["_id"] = str(sub["_id"])

#         return {
#             "message": "Submissions Retrieved Successfully!",
#             "data": submissions_list
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# def update_marks(id: str, marks: float):
#     try:
#         submission = submissions.find_one_and_update(
#             { "_id": ObjectId(id) },
#             {
#                 "$inc": { "marks": marks },
#                 "$set": { "status": "checked" }
#             },
#             return_document=ReturnDocument.AFTER
#         )

#         if not submission:
#             raise HTTPException(status_code=404, detail="Submission Not Found")

#         submission["_id"] = str(submission["_id"])

#         teacher_email = os.getenv("SIR_AMEEN_EMAIL")

#         email_content = submission.copy()

#         send_email_message(
#             teacher_email,
#             "Project Submission from BSCS Section 1A",
#             email_content
#         )


#         return {
#             "message": "Marks Updated and Email Sent Successfully!",
#             "data": submission
#         }

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
from database import connect_to_database
from models import Submission
from datetime import datetime
from fastapi import HTTPException, UploadFile, File, Form
from bson import ObjectId
from pymongo import ReturnDocument
from typing import List
from dotenv import load_dotenv
from mailer import send_email_message
from drive import create_folder, upload_file_to_folder, get_folder_link
import os
import shutil
import json

# Load environment variables
load_dotenv()

# Database setup
db = connect_to_database()
submissions = db.get_collection("submissions")

# Local temp upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------------------------------------
# SUBMIT PROJECT (STUDENT)
# --------------------------------------------------
def submit_project(data=None, files: List[UploadFile] = None):
    """
    Accepts either:
      - a `Submission` instance (programmatic call from main after files already uploaded),
      - or `data` as JSON string and `files` as uploaded files (when called as endpoint).
    """
    try:
        # Handle both programmatic Submission and multipart endpoint
        if isinstance(data, Submission):
            group_data = data
        else:
            # when called from FastAPI endpoint, `data` is a JSON string
            group_data = Submission.model_validate_json(data)

        # If files provided (endpoint case), upload them to Drive
        if files:
            # Create folder name using all student IDs
            student_ids = "_".join([m.student_id for m in group_data.members])
            folder_name = f"Project_{student_ids}"

            # Create or reuse Google Drive folder
            folder_id = create_folder(folder_name)

            # Save files locally → upload to Drive → delete local copy
            for file in files:
                local_path = os.path.join(UPLOAD_DIR, file.filename)

                with open(local_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                upload_file_to_folder(local_path, file.filename, folder_id)

                os.remove(local_path)

            # Save Drive folder link in DB
            group_data.project_details.code_file_path = get_folder_link(folder_id)

        # Auto marks logic
        deadline = datetime(2026, 1, 1)
        if datetime.now() < deadline:
            group_data.marks += 5

        result = submissions.insert_one(group_data.model_dump())

        return {
            "message": "Project Submitted Successfully!",
            "id": str(result.inserted_id),
            "drive_folder": group_data.project_details.code_file_path
        }

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Submit Error:", e)
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------------------------------
# GET SINGLE SUBMISSION
# --------------------------------------------------
def get_submission_details(id: str):
    try:
        submission = submissions.find_one({"_id": ObjectId(id)})

        if not submission:
            raise HTTPException(status_code=404, detail="Submission Not Found")

        submission["_id"] = str(submission["_id"])

        return {
            "message": "Submission Retrieved Successfully!",
            "data": submission
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------------------------------
# GET ALL SUBMISSIONS (ADMIN)
# --------------------------------------------------
def get_all_submissions():
    try:
        submissions_list = list(submissions.find({}))

        if not submissions_list:
            raise HTTPException(status_code=404, detail="Submissions Not Found")

        for sub in submissions_list:
            sub["_id"] = str(sub["_id"])

        return {
            "message": "Submissions Retrieved Successfully!",
            "data": submissions_list
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------------------------------
# UPDATE MARKS (ADMIN)
# --------------------------------------------------
def update_marks(id: str, marks: float):
    try:
        submission = submissions.find_one_and_update(
            {"_id": ObjectId(id)},
            {
                "$inc": {"marks": marks},
                "$set": {"status": "checked"}
            },
            return_document=ReturnDocument.AFTER
        )

        if not submission:
            raise HTTPException(status_code=404, detail="Submission Not Found")

        submission["_id"] = str(submission["_id"])

        # Email notification
        teacher_email = os.getenv("SIR_AMEEN_EMAIL")
        if teacher_email:
            send_email_message(
                teacher_email,
                "Project Submission Evaluated",
                submission
            )

        return {
            "message": "Marks Updated Successfully!",
            "data": submission
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
