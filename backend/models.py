from pydantic import BaseModel
from typing import List

class Project(BaseModel):
    title: str
    description: str
    code_file_path: str

class Student(BaseModel):
    student_name: str
    student_id: str

class Submission(BaseModel):
    members: List[Student]
    project_details: Project
    marks: float = 0
    status: str = "pending" 

class MarksUpdate(BaseModel):
    marks: float