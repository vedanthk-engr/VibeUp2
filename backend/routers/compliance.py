from fastapi import APIRouter, Request, Query, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.services.compliance_service import compliance_service

router = APIRouter(prefix="/compliance", tags=["BIS Compliance & Governance"])

class ConsentUpdateRequest(BaseModel):
    user_id: Optional[str] = "default_user"
    consent_type: str
    granted: bool

class BatchConsentRequest(BaseModel):
    user_id: Optional[str] = "default_user"
    consents: Dict[str, bool]

class ErasureRequest(BaseModel):
    user_id: Optional[str] = "default_user"
    confirm_text: str  # Must match "DELETE MY DATA"

@router.get("/status")
def get_compliance_status():
    """
    Returns full BIS (Bureau of Indian Standards) & BIS (Bank for International Settlements)
    compliance certification matrix. Covers IS 17428, IS/ISO 42001, IS/ISO 27001, and BCBS 239.
    """
    return compliance_service.get_compliance_matrix()

@router.get("/consent")
def get_user_consents(user_id: str = Query("default_user")):
    """
    Retrieves IS 17428 consent state for a user per DPDP Act 2023 specifications.
    """
    return compliance_service.get_user_consents(user_id)

@router.post("/consent")
def update_user_consent(req: ConsentUpdateRequest, request: Request):
    """
    Updates a specific consent option with client IP hashing for compliance proof.
    """
    client_ip = request.client.host if request.client else "unknown"
    return compliance_service.record_consent(
        user_id=req.user_id or "default_user",
        consent_type=req.consent_type,
        granted=req.granted,
        client_ip=client_ip
    )

@router.post("/consent/batch")
def batch_update_consents(req: BatchConsentRequest, request: Request):
    """
    Updates multiple consents in one call.
    """
    client_ip = request.client.host if request.client else "unknown"
    results = {}
    for c_type, granted in req.consents.items():
        results[c_type] = compliance_service.record_consent(
            user_id=req.user_id or "default_user",
            consent_type=c_type,
            granted=granted,
            client_ip=client_ip
        )
    return {"status": "SUCCESS", "updated": results}

@router.get("/audit-logs")
def get_ai_audit_logs(limit: int = Query(15, ge=1, le=100)):
    """
    Retrieves recent algorithmic inference audit trails per IS/ISO/IEC 42001:2023.
    Demonstrates model provenance and SEBI RAG citations.
    """
    return compliance_service.get_recent_audit_logs(limit=limit)

@router.post("/export-data")
def export_user_data(user_id: str = Query("default_user")):
    """
    Fulfills IS 17428 / DPDP Act Right to Data Portability.
    Exports all stored financial settings, history, and consent records.
    """
    return compliance_service.export_user_data(user_id)

@router.post("/erasure")
def request_erasure(req: ErasureRequest):
    """
    Fulfills IS 17428 / DPDP Act Right to Erasure ('Right to be Forgotten').
    Permanently purges chat transcripts and personal memory.
    """
    if req.confirm_text.strip().upper() != "DELETE MY DATA":
        raise HTTPException(
            status_code=400,
            detail="To confirm data erasure, confirm_text must be exactly 'DELETE MY DATA'."
        )
    return compliance_service.process_erasure_request(req.user_id or "default_user")
