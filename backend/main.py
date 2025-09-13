# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Civic Sprint API")

# Allow frontend (Vite React app) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- MODELS ----------
class Issue(BaseModel):
    id: int
    title: str
    description: str
    status: str = "Pending"
    photo_url: Optional[str] = None

class IssueCreate(BaseModel):
    title: str
    description: str

# --------- FAKE DATABASE ----------
issues: List[Issue] = []
issue_counter = 1

# --------- ROUTES ----------

@app.get("/")
def root():
    return {"message": "Civic Sprint Backend is running 🚀"}

# Report a new issue
@app.post("/issues", response_model=Issue)
def report_issue(issue: IssueCreate):
    global issue_counter
    new_issue = Issue(
        id=issue_counter,
        title=issue.title,
        description=issue.description,
        status="Pending",
    )
    issues.append(new_issue)
    issue_counter += 1
    return new_issue

# List all issues
@app.get("/issues", response_model=List[Issue])
def list_issues():
    return issues

# Get issue by ID
@app.get("/issues/{issue_id}", response_model=Issue)
def get_issue(issue_id: int):
    for issue in issues:
        if issue.id == issue_id:
            return issue
    return {"error": "Issue not found"}

# Update issue status
@app.put("/issues/{issue_id}", response_model=Issue)
def update_issue(issue_id: int, status: str = Form(...)):
    for issue in issues:
        if issue.id == issue_id:
            issue.status = status
            return issue
    return {"error": "Issue not found"}

# Community dashboard summary
@app.get("/dashboard")
def dashboard():
    total = len(issues)
    resolved = len([i for i in issues if i.status.lower() == "resolved"])
    pending = total - resolved
    return {
        "total_issues": total,
        "resolved": resolved,
        "pending": pending,
    }
