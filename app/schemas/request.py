
from pydantic import BaseModel, EmailStr, Field


class EmailRequest(BaseModel):
    sender: str = Field(min_length=3, max_length=254)
    subject: str = Field(min_length=1, max_length=500)
    body: str = Field(min_length=1, max_length=20000)


class ApprovalRequest(BaseModel):
    approved_by: str = Field(min_length=1, max_length=254)
