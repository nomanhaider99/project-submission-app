from fastapi import APIRouter, FastAPI
from controllers import submit_project, update_marks, get_all_submissions, get_submission_details
from models import Submission, MarksUpdate

app = FastAPI()
router = APIRouter()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

@app.post("/api/submit-project")
def submit_project_endpoint(data: Submission):
    return submit_project(data)

@app.get("/api/get-submission-details/{id}")
def get_submission_details_endpoint(id: str):
    return get_submission_details(id)

@app.get("/api/get-all-submissions")
def get_all_submissions_endpoint():
    return get_all_submissions()

@app.patch("/api/update-marks/{id}")
def update_marks_endpoint(id: str, payload: MarksUpdate):
    return update_marks(id, payload.marks)

app.include_router(router)