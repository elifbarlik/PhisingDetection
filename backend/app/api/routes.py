"""
API routes for phishing detection
"""
from fastapi import APIRouter, HTTPException
from app.schemas import EmailCreate, AnalysisResponse
from app.services.feature_extractor import EmailFeatureExtractor
from app.services.ml_model import model

router = APIRouter(prefix="/api/v1", tags=["Analysis"])

extractor = EmailFeatureExtractor()


@router.post("/analyze/email", response_model=dict)
def analyze_email(email_data: EmailCreate):
    """
    Analyze email for phishing risk

    Takes raw email and returns risk assessment
    """
    pass