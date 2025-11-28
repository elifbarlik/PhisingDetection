# 🏗️ System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                         │
│            (Web UI + Real-time Dashboard)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│                   API Gateway (FastAPI)                      │
│          (Authentication, Rate Limiting, Routing)            │
└──────────┬────────────────────┬──────────────────────────────┘
           │                    │
    ┌──────▼──────┐      ┌──────▼──────┐
    │   REST API  │      │  WebSocket  │
    │  Endpoints  │      │   Handler   │
    └──────┬──────┘      └──────┬──────┘
           │                    │
┌──────────▼────────────────────▼──────────────────────────────┐
│                    Service Layer                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • Email Analysis Service     • URL Analysis        │   │
│  │  • Feature Extraction          • ML Prediction      │   │
│  │  • Threat Intelligence         • Report Generation  │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────┬───────────────────────────────────────────────────┘
           │
    ┌──────┴────────────┬──────────────────┬────────────┐
    │                   │                  │            │
┌───▼───┐   ┌──────────▼──┐   ┌──────────▼────┐  ┌────▼────┐
│  ML   │   │  Database   │   │  Cache Layer  │  │ Job     │
│ Models│   │ (PostgreSQL)│   │  (Redis)      │  │ Queue   │
└───┬───┘   └──────┬──────┘   └──────┬────────┘  │(Celery) │
    │              │                 │           └────┬────┘
    │              │                 │                │
    └──────────────┴─────────────────┴────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐  ┌──────▼──────┐ ┌────▼────┐
   │VirusTotal │  │ URLhaus    │ │PhishTank│
   │  API      │  │  API       │ │  API    │
   └───────────┘  └────────────┘ └─────────┘
```

## Components

### 1. Frontend Layer
- **React 18** TypeScript ile
- **TailwindCSS** styling
- **Axios** for API calls
- **Recharts** for visualizations
- **Context API** for state management

### 2. API Gateway
- **FastAPI** framework
- **JWT** authentication
- **Rate Limiting** middleware
- **Request Validation** (Pydantic)
- **CORS** handling
- **Error handling** middleware

### 3. Service Layer

#### Email Analysis Service
```
Raw Email Input
    ↓
[Header Parser] → SPF/DKIM/DMARC check
[Body Parser] → NLP analysis, sentiment
[Subject Parser] → Keyword detection
[Link Extractor] → URL analysis
    ↓
Feature Vector → ML Model
    ↓
Risk Score + Explanation
```

#### URL Analysis Service
```
URL Input
    ↓
[URL Parser] → Structure analysis
[Reputation Check] → VirusTotal, URLhaus
[SSL Check] → Certificate validation
[Redirect Detection] → Follow redirects
[Content Check] → Phishing keywords
    ↓
Feature Vector → ML Model
    ↓
Risk Score + Details
```

#### Feature Extraction
- **Email Headers**: Sender validation, SPF/DKIM/DMARC, consistency
- **Email Body**: Sentiment, entities, grammar, language
- **URLs**: Structure, reputation, SSL, redirects, typosquatting
- **Attachments**: Type, executable, macros, size

### 4. ML/AI Pipeline

#### Models
1. **XGBoost** (Tabular Features)
   - Input: 50+ engineered features
   - Output: Phishing probability (0-1)
   - Inference time: <100ms

2. **BERT-based NLP** (Text Analysis)
   - Input: Email subject + body
   - Output: Text risk score
   - Fine-tuned on phishing dataset

3. **Ensemble**
   - Weighted combination of above
   - Final confidence score

#### Training Pipeline
```
Raw Dataset
    ↓
[Data Cleaning] → Handle missing values
[Feature Engineering] → Extract 50+ features
[Train/Test Split] → 70/15/15
    ↓
[Model Training] → XGBoost, BERT
[Hyperparameter Tuning] → GridSearch
[Evaluation] → Accuracy, Precision, Recall, F1
    ↓
[Model Versioning] → MLflow registry
```

### 5. Data Layer

#### Database Schema
```
users
  ├── id (PK)
  ├── email (UNIQUE)
  ├── password (hashed)
  ├── role (admin/user)
  └── created_at

emails
  ├── id (PK)
  ├── user_id (FK)
  ├── raw_email
  ├── sender
  ├── subject
  └── received_at

analyses
  ├── id (PK)
  ├── email_id (FK)
  ├── risk_score (0-1)
  ├── risk_level (HIGH/MEDIUM/LOW)
  ├── confidence
  ├── features (JSON)
  ├── explanation
  └── created_at

urls
  ├── id (PK)
  ├── url
  ├── reputation_score
  ├── is_malicious
  └── last_checked

threats
  ├── id (PK)
  ├── threat_type
  ├── severity
  ├── indicators
  └── last_seen
```

#### Indexes
```
emails.user_id
emails.received_at
analyses.user_id
analyses.risk_score
urls.url (UNIQUE)
threats.threat_type
```

### 6. Cache Layer (Redis)

```
Analysis Results Cache: analysis:{id} → JSON
URL Reputation Cache: url_rep:{url} → Score
Model Predictions Cache: pred:{hash} → Score
Session Cache: session:{token} → UserData
Rate Limit Counter: rate:{ip} → Count
```

### 7. Job Queue (Celery + Redis)

```
Celery Tasks:
  - bulk_email_analysis()
  - model_retraining()
  - threat_intelligence_update()
  - report_generation()
  - old_data_cleanup()
```

## Data Flow

### Email Analysis Flow
```
POST /api/v1/analyze/email
    ↓
[Auth Middleware] → Validate token
[Input Validation] → Check email format
[Rate Limiting] → Check quota
    ↓
[Email Parser] → Extract headers, body, links
[Feature Extraction] → Generate feature vector
    ↓
[Cache Check] → Check if seen before
[ML Model] → Predict risk score
[Explanation] → Generate insights
    ↓
[Database] → Store analysis result
[Cache] → Cache result
    ↓
GET /analysis/{id}
    ↓
Return Result + Explanation
```

### Training Flow
```
Scheduled Job (weekly)
    ↓
[Data Collector] → Fetch recent emails
[Data Cleaner] → Remove duplicates
[Feature Engineering] → Extract features
    ↓
[Model Training] → Train on new data
[Evaluation] → Test on validation set
    ↓
Performance > Threshold?
    ├─ YES → Deploy new model
    └─ NO → Keep current model
    ↓
[Model Registry] → Store version
[Monitoring] → Alert on issues
```

## External Integrations

### VirusTotal API
- URL reputation scanning
- File analysis
- Domain information

### PhishTank API
- Phishing URL database
- Threat intelligence updates

### URLhaus API
- Malicious URL detection
- IP reputation

### Email Verification Service
- SPF/DKIM/DMARC validation
- Domain existence check

## Security Architecture

### Authentication & Authorization
```
Login Request
    ↓
[Validate Credentials] → Check database
[Generate JWT] → Secret token
    ↓
Token Stored (Frontend)
    ↓
Every Request
    ↓
[Verify JWT] → Check signature & expiry
[Extract User] → Get user info
[Check Permissions] → Role-based access
    ↓
Allow/Deny
```

### Data Protection
- Database: Encrypted at rest (PostgreSQL pgcrypto)
- Transit: TLS 1.3 (HTTPS)
- Passwords: Bcrypt hashing
- Sensitive Data: Column-level encryption

### API Security
- Rate Limiting: 100 requests/minute per user
- CORS: Whitelist frontend domains
- CSRF: Token validation
- Input Validation: Pydantic models
- SQL Injection: SQLAlchemy ORM (parameterized queries)
- XSS: React auto-escaping

## Scalability Architecture

### Horizontal Scaling
```
Load Balancer (Nginx)
    ↓
┌───────┬───────┬───────┐
│API-1  │API-2  │API-3  │
└───────┴───────┴───────┘
    ↓
PostgreSQL (Primary)
    ├─ Read Replica 1
    └─ Read Replica 2
```

### Database Optimization
- Connection pooling (PgBouncer)
- Query caching (Redis)
- Materialized views for reports
- Partitioning by date for large tables

### Caching Strategy
- **L1 Cache**: Redis (API response cache)
- **L2 Cache**: Browser cache (static assets)
- **Database Query Cache**: Redis for frequently accessed data

## Monitoring & Observability

### Metrics
- API response time
- Model inference time
- Database query performance
- Error rates
- User activity
- Resource utilization

### Logging
- Application logs: FastAPI logger
- Access logs: Nginx
- Error tracking: Sentry
- Audit logs: Database triggers

### Alerting
- CPU/Memory > 80%
- Error rate > 1%
- Response time > 1s
- Model accuracy drop

## Disaster Recovery

### Backup Strategy
- Database: Daily snapshots + WAL archiving
- Models: Version control + registry
- Code: Git repository

### Recovery RTO/RPO
- RTO: 1 hour
- RPO: 15 minutes

## Deployment Pipeline

```
Local Development
    ↓
Git Push
    ↓
GitHub Actions
    ├─ Lint
    ├─ Test
    ├─ Build Docker images
    └─ Push to registry
    ↓
Staging Environment
    ├─ Deploy
    └─ Run integration tests
    ↓
Production Deployment
    ├─ Blue-green deployment
    └─ Health checks
```

## Performance Targets

| Metric | Target | Monitoring |
|--------|--------|-----------|
| API Response | <500ms p95 | Prometheus |
| Model Inference | <100ms | Application logs |
| DB Query | <50ms p95 | PostgreSQL metrics |
| Page Load | <2s | Frontend monitoring |
| Uptime | 99.9% | Healthchecks |
| Error Rate | <0.1% | Error tracking |

---

Next: Database schema detaylı tasarımı ve API endpoints mapping'i yapacağız.
