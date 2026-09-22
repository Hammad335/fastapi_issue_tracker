import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueOut, IssueUpdate, IssueStatus
from app.storage import load_data, save_data 

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

@router.get("/", response_model=list[IssueOut])
async def get_issues():
    """Get all issues"""
    issues = load_data()
    return issues

@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(issue: IssueCreate):
    """Create a new issue"""
    issues = load_data()
    new_issue = IssueOut(
        id= str(uuid.uuid4()),
        title= issue.title,
        description= issue.description,
        priority= issue.priority,
        status= IssueStatus.open
    )

    issues.append(new_issue.model_dump())
    save_data(issues)

    return new_issue

@router.get("/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: str):
    """Get a specific issue by ID"""

    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            return issue 

    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: str, issue_update: IssueUpdate):
    """Update a specific issue by ID"""

    issues= load_data()
    for index, issue in enumerate(issues):
        if (issue["id"] == issue_id):
            updated_issue = issue.copy()

            if (issue_update.title is not None):
                updated_issue["title"]= issue_update.title
            if (issue_update.description is not None):
                updated_issue["description"]= issue_update.description
            if (issue_update.priority is not None):
                updated_issue["priority"]= issue_update.priority
            if (issue_update.status is not None):
                updated_issue["status"]= issue_update.status

            issues[index]= updated_issue
            save_data(issues)
            return updated_issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: str):
    """Delete an issue by ID"""

    issues = load_data()

    for index, issue in enumerate(issues):
        if (issue["id"] == issue_id):
            issues.pop(index)
            save_data(issues)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

    