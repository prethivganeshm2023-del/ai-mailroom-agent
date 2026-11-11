
import json

from fastapi import APIRouter, HTTPException

from app.schemas.request import EmailRequest, ApprovalRequest
from app.database.db import (
    save_email,
    update_email,
    get_emails,
    get_email,
    log_event,
    get_audit_logs
)
from app.services.agent import generate_analysis


router = APIRouter(prefix="/api", tags=["Mailroom"])


@router.post("/emails")
def receive_email(request: EmailRequest):

    # Save incoming email
    email_id = save_email(
        request.sender,
        request.subject,
        request.body
    )

    log_event(email_id, "EMAIL_RECEIVED")

    # Analyse email
    analysis = generate_analysis(
        request.sender,
        request.subject,
        request.body
    )

    action = analysis["recommended_action"]

    if action == "quarantine":
        status = "quarantined"

    elif action == "human_review":
        status = "pending_review"

    elif action == "draft_reply":
        status = "draft_pending_review"

    else:
        status = "processed"

    analysis_json = json.dumps(analysis)

    update_email(
        email_id,
        status,
        analysis_json
    )

    log_event(
        email_id,
        "AI_ANALYSIS_COMPLETED",
        analysis_json
    )

    return {
        "email_id": email_id,
        "status": status,
        "analysis": analysis
    }


@router.get("/emails")
def list_emails():

    return {
        "emails": get_emails()
    }


@router.get("/emails/{email_id}")
def email_details(email_id: int):

    email = get_email(email_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    email["audit_logs"] = get_audit_logs(email_id)

    return email


@router.post("/emails/{email_id}/approve")
def approve_email(
    email_id: int,
    request: ApprovalRequest
):

    email = get_email(email_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    if email["status"] not in {
        "pending_review",
        "draft_pending_review"
    }:
        raise HTTPException(
            status_code=409,
            detail="Email is not awaiting approval"
        )

    update_email(
        email_id,
        "approved",
        email["analysis"]
    )

    log_event(
        email_id,
        "HUMAN_APPROVED",
        request.approved_by
    )

    return {
        "email_id": email_id,
        "status": "approved",
        "approved_by": request.approved_by,
        "message": "Approval recorded. No email was sent."
    }
