from database import connect_to_database
from models import Submission
from datetime import datetime
from fastapi import HTTPException
from mailer import send_email_message
from dotenv import load_dotenv
import os
from bson import ObjectId
from pymongo import ReturnDocument

load_dotenv()

db = connect_to_database()
submissions = db.get_collection("submissions")

def submit_project(group_data: Submission):
    try:
        current_time = datetime.now()
        deadline = datetime(2026, 1, 1)

        if current_time < deadline:
            group_data.marks += 5

        result = submissions.insert_one(group_data.model_dump())

        return {
            "message": "Project Submitted Successfully!",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_submission_details(id: str):
    try:
        submission = submissions.find_one({ "_id": ObjectId(id) })

        if not submission:
            raise HTTPException(status_code=404, detail="Submission Not Found")

        submission["_id"] = str(submission["_id"])

        return {
            "message": "Submission Retrieved Successfully!",
            "data": submission
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_marks(id: str, marks: float):
    try:
        submission = submissions.find_one_and_update(
            { "_id": ObjectId(id) },
            {
                "$inc": { "marks": marks },
                "$set": { "status": "checked" }
            },
            return_document=ReturnDocument.AFTER
        )

        if not submission:
            raise HTTPException(status_code=404, detail="Submission Not Found")

        submission["_id"] = str(submission["_id"])

        teacher_email = os.getenv("SIR_AMEEN_EMAIL")

        email_content = submission.copy()

        send_email_message(
            teacher_email,
            "Project Submission from BSCS Section 1A",
            email_content
        )


        return {
            "message": "Marks Updated and Email Sent Successfully!",
            "data": submission
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
