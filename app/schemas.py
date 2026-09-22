from enum import Enum
# Field is used to add validation such as min_length etc and metadata to model attributes
from pydantic import BaseModel, Field 
from typing import Optional

class IssueStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"

class IssuePriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class IssueCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    priority: IssuePriority = IssuePriority.medium

class IssueUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=5, max_length=100)
    description: Optional[str] = Field(default=None, min_length=10, max_length=1000)
    status: Optional[IssueStatus] = None
    priority: Optional[IssuePriority] = None

class IssueOut(BaseModel):
    id: str
    title: str
    description: str
    priority: IssuePriority
    status: IssueStatus