# 📊 Database Schema Design

## ER Diagram

```
┌──────────────┐
│    users     │
├──────────────┤
│ id (PK)      │
│ email        │◄──┐
│ password     │   │
│ first_name   │   │
│ last_name    │   │ 1:N
│ role         │   │
│ is_active    │   │
│ created_at   │   │
│ updated_at   │   │
└──────────────┘   │
       ▲           │
       │           │
       │     ┌─────────────────┐
       │     │    emails       │
       │     ├─────────────────┤
       │     │ id (PK)         │
       │     │ user_id (FK)────┘
       │     │ raw_email       │
       │     │ sender          │
       │     │ recipient       │
       │     │ subject         │
       │     │ body            │
       │     │ received_at     │
       └─────│ created_at      │
             └─────────────────┘
                     │
                     │ 1:N
                     ▼
           ┌──────────────────────┐
           │    analyses          │
           ├──────────────────────┤
           │ id (PK)              │
           │ email_id (FK)        │
           │ risk_score (0-1)     │
           │ risk_level           │
           │ confidence           │
           │ features (JSON)      │
           │ explanation          │
           │ model_version        │
           │ created_at           │
           └──────────────────────┘

┌──────────────────┐
│    urls          │
├──────────────────┤
│ id (PK)          │
│ url (UNIQUE)     │
│ domain           │
│ reputation_score │
│ is_malicious     │
│ last_checked     │
│ virusTotal_data  │
│ urlhaus_data     │
│ created_at       │
└──────────────────┘

┌──────────────────┐
│    threats       │
├──────────────────┤
│ id (PK)          │
│ threat_type      │
│ severity         │
│ indicators (JSON)│
│ first_seen       │
│ last_seen        │
│ count            │
│ description      │
└──────────────────┘

┌──────────────────┐
│    api_logs      │
├──────────────────┤
│ id (PK)          │
│ user_id (FK)     │
│ endpoint         │
│ method           │
│ status_code      │
│ response_time    │
│ created_at       │
└──────────────────┘
```

## Detailed Schema

### 1. users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(20) CHECK (role IN ('admin', 'user')) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

**Columns:**
- `id`: Unique identifier
- `email`: User email (login credential)
- `password`: Hashed password (Bcrypt)
- `first_name`, `last_name`: User name
- `role`: admin or user
- `is_active`: Soft delete flag
- `created_at`, `updated_at`: Timestamps

---

### 2. emails Table

```sql
CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    raw_email TEXT NOT NULL,
    sender VARCHAR(255) NOT NULL,
    recipient VARCHAR(255),
    subject VARCHAR(500),
    body TEXT,
    headers JSONB,
    received_at TIMESTAMP,
    is_flagged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_emails_user_id ON emails(user_id);
CREATE INDEX idx_emails_sender ON emails(sender);
CREATE INDEX idx_emails_received_at ON emails(received_at);
CREATE INDEX idx_emails_created_at ON emails(created_at);
```

**Columns:**
- `id`: Unique email ID
- `user_id`: User who uploaded email
- `raw_email`: Complete email in MIME format
- `sender`: Email sender address
- `recipient`: Email recipient
- `subject`: Email subject
- `body`: Email body (plain text)
- `headers`: JSON object with all headers
- `received_at`: When email was received
- `is_flagged`: User flagged as suspicious
- `created_at`: When uploaded to platform

**Headers JSON Structure:**
```json
{
  "from": "sender@example.com",
  "to": "recipient@example.com",
  "date": "2024-01-15T10:30:00Z",
  "subject": "Verify your account",
  "return_path": "bounces@example.com",
  "reply_to": "noreply@example.com",
  "received": [
    {
      "from": "mail.example.com",
      "by": "mx.recipient.com",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "authentication_results": {
    "spf": "pass",
    "dkim": "pass",
    "dmarc": "pass"
  }
}
```

---

### 3. analyses Table

```sql
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    email_id INTEGER UNIQUE NOT NULL REFERENCES emails(id) ON DELETE CASCADE,
    risk_score DECIMAL(3,2) CHECK (risk_score >= 0 AND risk_score <= 1),
    risk_level VARCHAR(20) CHECK (risk_level IN ('HIGH', 'MEDIUM', 'LOW')),
    confidence DECIMAL(3,2) CHECK (confidence >= 0 AND confidence <= 1),
    features JSONB,
    explanation JSONB,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time_ms INTEGER
);

-- Indexes
CREATE INDEX idx_analyses_email_id ON analyses(email_id);
CREATE INDEX idx_analyses_risk_score ON analyses(risk_score);
CREATE INDEX idx_analyses_created_at ON analyses(created_at);
```

**Columns:**
- `email_id`: Reference to analyzed email
- `risk_score`: 0-1 probability of phishing
- `risk_level`: HIGH (>0.7), MEDIUM (0.3-0.7), LOW (<0.3)
- `confidence`: Model confidence (0-1)
- `features`: Extracted features used for prediction
- `explanation`: Why it's flagged (for user)
- `model_version`: Which model was used
- `processing_time_ms`: Analysis duration
- `created_at`: When analysis was done

**Features JSON Structure:**
```json
{
  "sender_features": {
    "domain_age_days": 365,
    "spf_valid": true,
    "dkim_valid": true,
    "dmarc_valid": true,
    "domain_reputation": 0.95
  },
  "header_features": {
    "header_consistency": 0.85,
    "suspicious_return_path": false
  },
  "subject_features": {
    "urgency_keywords": 2,
    "length": 28
  },
  "body_features": {
    "sentiment_score": -0.4,
    "typos_count": 1,
    "entities_count": 3,
    "suspicious_links": 1
  },
  "url_features": {
    "urls_in_email": 2,
    "malicious_urls": 0
  }
}
```

**Explanation JSON Structure:**
```json
{
  "risk_factors": [
    "Suspicious urgency keywords in subject",
    "Domain not verified (SPF failed)",
    "Links point to different domain"
  ],
  "safe_indicators": [
    "DKIM signature valid",
    "No executable attachments"
  ],
  "summary": "Email shows signs of phishing attack targeting account verification"
}
```

---

### 4. urls Table

```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    url VARCHAR(2048) UNIQUE NOT NULL,
    domain VARCHAR(255),
    reputation_score DECIMAL(3,2),
    is_malicious BOOLEAN,
    last_checked TIMESTAMP,
    virusTotal_data JSONB,
    urlhaus_data JSONB,
    ssl_valid BOOLEAN,
    ssl_certificate_data JSONB,
    phishtank_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_urls_domain ON urls(domain);
CREATE INDEX idx_urls_reputation ON urls(reputation_score);
CREATE INDEX idx_urls_last_checked ON urls(last_checked);
```

**Columns:**
- `url`: Full URL
- `domain`: Extracted domain
- `reputation_score`: Combined reputation (0-1)
- `is_malicious`: Flagged as malicious
- `last_checked`: When reputation was last checked
- `virusTotal_data`: API response from VirusTotal
- `urlhaus_data`: Data from URLhaus
- `ssl_valid`: SSL certificate validity
- `ssl_certificate_data`: Certificate details
- `phishtank_data`: Data from PhishTank

---

### 5. threats Table

```sql
CREATE TABLE threats (
    id SERIAL PRIMARY KEY,
    threat_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) CHECK (severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
    indicators JSONB NOT NULL,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    count INTEGER DEFAULT 1,
    description TEXT,
    source VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
);

-- Indexes
CREATE INDEX idx_threats_threat_type ON threats(threat_type);
CREATE INDEX idx_threats_severity ON threats(severity);
CREATE INDEX idx_threats_last_seen ON threats(last_seen DESC);
```

**Threat Types:**
- Email phishing campaign
- Malicious URL detected
- Typosquatting domain
- CEO fraud
- Credential harvesting

**Indicators JSON:**
```json
{
  "keywords": ["verify account", "confirm password"],
  "domains": ["suspicious-bank.com"],
  "sender_patterns": ["noreply@*"],
  "attachment_types": [".exe", ".scr"]
}
```

---

### 6. api_logs Table

```sql
CREATE TABLE api_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER,
    response_time_ms INTEGER,
    request_data JSONB,
    error_message TEXT,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_api_logs_user_id ON api_logs(user_id);
CREATE INDEX idx_api_logs_endpoint ON api_logs(endpoint);
CREATE INDEX idx_api_logs_created_at ON api_logs(created_at);
CREATE INDEX idx_api_logs_status ON api_logs(status_code);
```

---

### 7. rate_limit_tracker Table

```sql
CREATE TABLE rate_limit_tracker (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    analysis_count INTEGER DEFAULT 0,
    reset_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_rate_limit_user ON rate_limit_tracker(user_id);
```

---

## Relationships

| From | To | Type | Cardinality |
|------|----|----- |-------------|
| users | emails | Foreign Key | 1:N |
| users | api_logs | Foreign Key | 1:N |
| users | rate_limit_tracker | Foreign Key | 1:N |
| emails | analyses | Foreign Key | 1:1 |

## Indexing Strategy

**High Priority Indexes** (Frequently searched):
- `emails.user_id` - Filter by user
- `analyses.risk_score` - Filter by risk
- `analyses.created_at` - Filter by date
- `urls.domain` - Domain lookups
- `threats.threat_type` - Threat filtering

**Medium Priority**:
- `emails.sender` - Sender analysis
- `api_logs.user_id` - User activity tracking
- `users.email` - Login

**Low Priority** (Less frequent):
- `emails.received_at` - Historical data

## Constraints & Validations

### Data Types
```python
risk_score: Decimal (0.00 - 1.00)
confidence: Decimal (0.00 - 1.00)
reputation_score: Decimal (0.00 - 1.00)
response_time_ms: Integer
```

### Check Constraints
```
risk_level IN ('HIGH', 'MEDIUM', 'LOW')
role IN ('admin', 'user')
severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')
method IN ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')
```

### Required Fields (NOT NULL)
- users: email, password
- emails: user_id, raw_email, sender
- analyses: email_id, risk_score, risk_level
- urls: url, domain
- threats: threat_type, indicators

## Partitioning Strategy

For large tables (emails, analyses), use time-based partitioning:

```sql
-- Partition by month
CREATE TABLE analyses_2024_01 PARTITION OF analyses
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE analyses_2024_02 PARTITION OF analyses
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

## Migration Strategy

Use Alembic for schema migrations:

```
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

---

Next: API Endpoints mapping ve data validation rules.
