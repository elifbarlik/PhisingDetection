"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, EmailStr, Field


# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """User response schema"""
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== AUTH SCHEMAS ====================

class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


# ==================== EMAIL SCHEMAS ====================

class EmailBase(BaseModel):
    """Base email schema"""
    sender: str
    recipient: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None


class EmailCreate(BaseModel):
    """Email creation schema"""
    raw_email: str = Field(..., description="Raw email in MIME format")


class EmailResponse(EmailBase):
    """Email response schema"""
    id: int
    user_id: int
    is_flagged: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== ANALYSIS SCHEMAS ====================

class RiskFactors(BaseModel):
    """Risk factors explanation"""
    risk_factors: List[str]
    safe_indicators: List[str]
    summary: str


class AnalysisBase(BaseModel):
    """Base analysis schema"""
    risk_score: float = Field(..., ge=0, le=1)
    risk_level: str = Field(..., pattern="^(HIGH|MEDIUM|LOW)$")
    confidence: float = Field(..., ge=0, le=1)


class AnalysisResponse(AnalysisBase):
    """Analysis response schema"""
    id: int
    email_id: int
    features: Optional[Dict[str, Any]] = None
    explanation: Optional[RiskFactors] = None
    model_version: Optional[str] = None
    processing_time_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisWithEmail(BaseModel):
    """Analysis with email details"""
    email: EmailResponse
    analysis: AnalysisResponse


# ==================== URL SCHEMAS ====================

class URLBase(BaseModel):
    """Base URL schema"""
    url: str


class URLAnalysisRequest(URLBase):
    """URL analysis request schema"""
    pass


class URLReputation(BaseModel):
    """URL reputation schema"""
    reputation_score: Optional[float] = None
    is_malicious: Optional[bool] = None
    sources: Optional[Dict[str, Any]] = None


class URLResponse(URLBase):
    """URL response schema"""
    id: int
    domain: Optional[str] = None
    reputation: Optional[URLReputation] = None
    ssl_valid: Optional[bool] = None
    last_checked: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== THREAT SCHEMAS ====================

class ThreatBase(BaseModel):
    """Base threat schema"""
    threat_type: str
    severity: str = Field(..., pattern="^(CRITICAL|HIGH|MEDIUM|LOW)$")
    description: Optional[str] = None
    indicators: Dict[str, Any]


class ThreatCreate(ThreatBase):
    """Threat creation schema"""
    pass


class ThreatResponse(ThreatBase):
    """Threat response schema"""
    id: int
    first_seen: datetime
    last_seen: datetime
    count: int
    is_active: bool

    class Config:
        from_attributes = True


# ==================== BATCH OPERATIONS ====================

class BatchEmailAnalysisRequest(BaseModel):
    """Batch email analysis request"""
    emails: List[str] = Field(..., description="List of raw emails")


class BatchURLAnalysisRequest(BaseModel):
    """Batch URL analysis request"""
    urls: List[str] = Field(..., min_items=1, max_items=100)


class BatchResponse(BaseModel):
    """Batch operation response"""
    batch_id: str
    total_items: int
    status: str  # processing, completed, failed
    progress: Optional[Dict[str, int]] = None


# ==================== PAGINATED RESPONSES ====================

class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    total: int
    page: int
    limit: int
    total_pages: int
    data: List[Any]


# ==================== ERROR RESPONSES ====================

class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==================== HEALTH CHECK ====================

class HealthResponse(BaseModel):
    """Health check response"""
    status: str  # healthy, degraded, unhealthy
    version: str
    environment: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)