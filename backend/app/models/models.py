"""
Database models for Phishing Detection Platform
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model - Platform users"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(20), default="user")  # admin, user
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    emails = relationship("Email", back_populates="user", cascade="all, delete-orphan")
    api_logs = relationship("APILog", back_populates="user", cascade="all, delete-orphan")
    rate_limit_tracker = relationship("RateLimitTracker", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


class Email(Base):
    """Email model - Analyzed emails"""
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    raw_email = Column(Text, nullable=False)
    sender = Column(String(255), nullable=False, index=True)
    recipient = Column(String(255))
    subject = Column(String(500))
    body = Column(Text)
    headers = Column(JSON)  # Stores email headers as JSON
    received_at = Column(DateTime)
    is_flagged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="emails")
    analysis = relationship("Analysis", back_populates="email", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Email {self.id} - {self.sender}>"


class Analysis(Base):
    """Analysis model - Email analysis results"""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    risk_score = Column(Float, nullable=False)  # 0-1
    risk_level = Column(String(20), nullable=False)  # HIGH, MEDIUM, LOW
    confidence = Column(Float, nullable=False)  # 0-1
    features = Column(JSON)  # Extracted features
    explanation = Column(JSON)  # Risk explanation for user
    model_version = Column(String(50))
    processing_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    email = relationship("Email", back_populates="analysis")

    def __repr__(self):
        return f"<Analysis {self.id} - {self.risk_level}>"


class URL(Base):
    """URL model - URL reputation cache"""
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), unique=True, nullable=False, index=True)
    domain = Column(String(255), index=True)
    reputation_score = Column(Float)  # 0-1
    is_malicious = Column(Boolean)
    last_checked = Column(DateTime)
    virusTotal_data = Column(JSON)
    urlhaus_data = Column(JSON)
    ssl_valid = Column(Boolean)
    ssl_certificate_data = Column(JSON)
    phishtank_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<URL {self.domain}>"


class Threat(Base):
    """Threat model - Threat intelligence"""
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    threat_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(20), nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    indicators = Column(JSON, nullable=False)  # Keywords, domains, patterns
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    count = Column(Integer, default=1)
    description = Column(Text)
    source = Column(String(100))  # community, internal, etc
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Threat {self.threat_type}>"


class APILog(Base):
    """APILog model - API request logging"""
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    endpoint = Column(String(255), nullable=False, index=True)
    method = Column(String(10), nullable=False)  # GET, POST, PUT, DELETE, PATCH
    status_code = Column(Integer, index=True)
    response_time_ms = Column(Integer)
    request_data = Column(JSON)
    error_message = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="api_logs")

    def __repr__(self):
        return f"<APILog {self.method} {self.endpoint} {self.status_code}>"


class RateLimitTracker(Base):
    """RateLimitTracker model - Rate limiting"""
    __tablename__ = "rate_limit_tracker"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    analysis_count = Column(Integer, default=0)
    reset_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="rate_limit_tracker")

    def __repr__(self):
        return f"<RateLimitTracker user_id={self.user_id}>"