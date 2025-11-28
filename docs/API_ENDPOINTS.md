# 🔌 API Endpoints Reference

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication Endpoints

### 1. User Registration
```
POST /auth/register
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error (400):**
```json
{
  "detail": "Email already exists"
}
```

---

### 2. User Login
```
POST /auth/login
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

### 3. Token Refresh
```
POST /auth/refresh
```

**Request Headers:**
```
Authorization: Bearer {refresh_token}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}
```

---

### 4. Logout
```
POST /auth/logout
```

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

---

## Email Analysis Endpoints

### 5. Analyze Email
```
POST /analyze/email
```

**Request Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
email_file: <.eml file or raw email text>
OR
raw_email: "From: sender@example.com\nTo: recipient@example.com\n..."
```

**Response (202 Accepted):**
```json
{
  "id": 101,
  "status": "processing",
  "message": "Email is being analyzed",
  "estimated_time_ms": 500
}
```

**Response After Completion (GET /analyze/email/{id}):**
```json
{
  "id": 101,
  "email": {
    "id": 50,
    "sender": "noreply@suspicious-bank.com",
    "subject": "Verify Your Account",
    "received_at": "2024-01-15T10:30:00Z"
  },
  "analysis": {
    "id": 101,
    "risk_score": 0.87,
    "risk_level": "HIGH",
    "confidence": 0.92,
    "explanation": {
      "summary": "This email shows strong indicators of phishing attack",
      "risk_factors": [
        "Domain not authenticated (SPF failed)",
        "Urgency keywords in subject line",
        "Links point to suspicious domain"
      ],
      "safe_indicators": [
        "No executable attachments"
      ]
    },
    "features": {
      "sender_features": {...},
      "header_features": {...},
      "subject_features": {...},
      "body_features": {...}
    },
    "suspicious_links": [
      {
        "url": "https://suspicious-bank.com/verify",
        "reputation": 0.15,
        "malicious": true
      }
    ],
    "created_at": "2024-01-15T10:31:00Z",
    "processing_time_ms": 245
  }
}
```

---

### 6. Get Analysis Result
```
GET /analyze/{id}
```

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 101,
  "email": {...},
  "analysis": {...}
}
```

---

### 7. List Analysis History
```
GET /analyze/history?page=1&limit=20&risk_level=HIGH&sort_by=created_at
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)
- `risk_level`: Filter by HIGH, MEDIUM, LOW
- `sort_by`: created_at, risk_score (default: created_at)
- `sort_order`: asc, desc (default: desc)
- `from_date`: ISO date filter
- `to_date`: ISO date filter

**Response (200 OK):**
```json
{
  "total": 245,
  "page": 1,
  "limit": 20,
  "total_pages": 13,
  "data": [
    {
      "id": 105,
      "email": {
        "sender": "attacker@example.com",
        "subject": "Urgent: Update Payment",
        "received_at": "2024-01-15T11:00:00Z"
      },
      "analysis": {
        "risk_score": 0.95,
        "risk_level": "HIGH",
        "confidence": 0.98,
        "created_at": "2024-01-15T11:01:00Z"
      }
    }
    // ... more results
  ]
}
```

---

### 8. Delete Analysis
```
DELETE /analyze/{id}
```

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (204 No Content):**
```
(empty body)
```

---

### 9. Batch Email Analysis
```
POST /analyze/batch/emails
```

**Request Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body:**
```
csv_file: <file with emails>
```

**CSV Format:**
```
sender,subject,body
sender@example.com,"Verify account","Click here..."
noreply@bank.com,"Security alert","Your account..."
```

**Response (202 Accepted):**
```json
{
  "batch_id": "batch_abc123",
  "total_emails": 100,
  "status": "processing",
  "progress": {
    "processed": 0,
    "total": 100
  }
}
```

---

## URL Analysis Endpoints

### 10. Analyze Single URL
```
POST /analyze/url
```

**Request Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://suspicious-bank.com/verify"
}
```

**Response (200 OK):**
```json
{
  "id": 200,
  "url": "https://suspicious-bank.com/verify",
  "domain": "suspicious-bank.com",
  "reputation": {
    "reputation_score": 0.15,
    "is_malicious": true,
    "sources": {
      "virusTotal": {
        "malicious_vendors": 45,
        "suspicious_vendors": 12,
        "clean_vendors": 3
      },
      "urlhaus": {
        "threat_type": "phishing",
        "payload": "credential_harvester"
      },
      "phishTank": {
        "verified": true,
        "phish_id": "5123456"
      }
    }
  },
  "ssl": {
    "valid": false,
    "certificate_data": {
      "issuer": "Unknown",
      "valid_until": "2024-12-31"
    }
  },
  "analysis": {
    "structure_analysis": {
      "has_at_symbol": false,
      "subdomain_count": 1,
      "uses_ip": false
    },
    "typosquatting_score": 0.8,
    "last_checked": "2024-01-15T10:30:00Z"
  },
  "created_at": "2024-01-15T10:31:00Z"
}
```

---

### 11. Batch URL Analysis
```
POST /analyze/urls/batch
```

**Request:**
```json
{
  "urls": [
    "https://example.com",
    "https://suspicious.com",
    "https://malicious.net"
  ]
}
```

**Response (202 Accepted):**
```json
{
  "batch_id": "batch_url_123",
  "urls": 3,
  "status": "processing"
}
```

**Get Batch Results:**
```
GET /analyze/batch/{batch_id}
```

---

### 12. URL History
```
GET /analyze/urls/history?limit=20
```

**Response:**
```json
{
  "total": 150,
  "data": [
    {
      "id": 200,
      "url": "https://suspicious.com",
      "reputation_score": 0.25,
      "is_malicious": true,
      "last_checked": "2024-01-15T10:30:00Z"
    }
    // ... more results
  ]
}
```

---

## Attachment Analysis Endpoints

### 13. Analyze Attachment
```
POST /analyze/attachment
```

**Request Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body:**
```
file: <binary file>
email_id: 50 (optional)
```

**Response (200 OK):**
```json
{
  "id": 300,
  "filename": "document.pdf",
  "file_type": "pdf",
  "file_size": 2048576,
  "analysis": {
    "is_malicious": false,
    "confidence": 0.98,
    "risk_factors": [],
    "details": {
      "has_macros": false,
      "is_executable": false,
      "mime_type_correct": true,
      "scan_results": {
        "virusTotal": {
          "malicious_vendors": 0,
          "suspicious_vendors": 0
        }
      }
    }
  },
  "created_at": "2024-01-15T10:31:00Z"
}
```

---

## User Management Endpoints

### 14. Get User Profile
```
GET /user/profile
```

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "is_active": true,
  "stats": {
    "total_analyses": 245,
    "high_risk_emails": 23,
    "avg_processing_time_ms": 350
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

---

### 15. Update User Profile
```
PUT /user/profile
```

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

---

### 16. Change Password
```
POST /user/change-password
```

**Request:**
```json
{
  "current_password": "old_password",
  "new_password": "new_secure_password"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

---

### 17. Get User Statistics
```
GET /user/statistics
```

**Response (200 OK):**
```json
{
  "total_analyses": 245,
  "analysis_by_risk": {
    "HIGH": 23,
    "MEDIUM": 65,
    "LOW": 157
  },
  "analysis_by_date": [
    {
      "date": "2024-01-15",
      "count": 12
    },
    {
      "date": "2024-01-14",
      "count": 8
    }
  ],
  "top_threats": [
    {
      "threat_type": "credential_harvesting",
      "count": 45
    },
    {
      "threat_type": "phishing",
      "count": 32
    }
  ],
  "avg_response_time_ms": 350
}
```

---

## Threat Intelligence Endpoints

### 18. Get Latest Threats
```
GET /threats/latest?limit=20
```

**Response (200 OK):**
```json
{
  "total": 1245,
  "data": [
    {
      "id": 1,
      "threat_type": "phishing_campaign",
      "severity": "HIGH",
      "description": "Bank impersonation campaign targeting EU users",
      "indicators": {
        "domains": ["bank-verify.com", "bank-secure.net"],
        "keywords": ["verify account", "confirm identity"]
      },
      "first_seen": "2024-01-10T00:00:00Z",
      "last_seen": "2024-01-15T15:30:00Z",
      "count": 1234,
      "source": "community"
    }
    // ... more threats
  ]
}
```

---

### 19. Get Threat Statistics
```
GET /threats/statistics?from_date=2024-01-01&to_date=2024-01-15
```

**Response (200 OK):**
```json
{
  "total_threats": 1245,
  "severity_distribution": {
    "CRITICAL": 12,
    "HIGH": 234,
    "MEDIUM": 567,
    "LOW": 432
  },
  "threat_types": {
    "phishing": 456,
    "malware": 234,
    "typosquatting": 123,
    "ceo_fraud": 89
  },
  "trends": [
    {
      "date": "2024-01-15",
      "new_threats": 45,
      "active_threats": 234
    }
  ],
  "geographic_distribution": {
    "US": 345,
    "EU": 234,
    "ASIA": 123
  }
}
```

---

### 20. Report New Threat
```
POST /threats/report
```

**Request:**
```json
{
  "threat_type": "phishing_campaign",
  "severity": "HIGH",
  "description": "Bank impersonation email campaign",
  "indicators": {
    "domains": ["suspicious-bank.com"],
    "sender_patterns": ["noreply@*suspicious*"],
    "keywords": ["verify account"]
  }
}
```

**Response (201 Created):**
```json
{
  "id": 1246,
  "message": "Threat reported successfully",
  "verification_status": "pending"
}
```

---

## Admin Endpoints

### 21. Get All Users (Admin Only)
```
GET /admin/users?page=1&limit=20
```

**Response:**
```json
{
  "total": 523,
  "data": [
    {
      "id": 1,
      "email": "user@example.com",
      "role": "user",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "stats": {
        "total_analyses": 245,
        "high_risk_emails": 23
      }
    }
    // ... more users
  ]
}
```

---

### 22. Get Platform Analytics (Admin Only)
```
GET /admin/analytics
```

**Response:**
```json
{
  "total_users": 523,
  "active_users": 412,
  "total_analyses": 45234,
  "total_high_risk": 3245,
  "avg_response_time_ms": 345,
  "model_performance": {
    "accuracy": 0.96,
    "precision": 0.94,
    "recall": 0.93,
    "f1_score": 0.935
  },
  "system_health": {
    "database_status": "healthy",
    "cache_status": "healthy",
    "api_uptime": 99.95
  }
}
```

---

### 23. Retrain Model (Admin Only)
```
POST /admin/model/retrain
```

**Response (202 Accepted):**
```json
{
  "job_id": "job_abc123",
  "status": "queued",
  "estimated_time_seconds": 3600,
  "message": "Model retraining job has been queued"
}
```

**Get Retraining Status:**
```
GET /admin/model/retrain/{job_id}
```

---

### 24. Get System Logs (Admin Only)
```
GET /admin/logs?endpoint=/analyze/email&status_code=500&limit=100
```

**Response:**
```json
{
  "total": 234,
  "data": [
    {
      "id": 1,
      "timestamp": "2024-01-15T10:30:00Z",
      "user_id": 1,
      "endpoint": "/analyze/email",
      "method": "POST",
      "status_code": 500,
      "response_time_ms": 1234,
      "error": "Database connection timeout"
    }
    // ... more logs
  ]
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `VALIDATION_ERROR` | 400 | Input validation failed |
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | User doesn't have permission |
| `NOT_FOUND` | 404 | Resource not found |
| `QUOTA_EXCEEDED` | 429 | User quota exceeded |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Rate Limiting

### Limits per User Tier

| Tier | Requests/Hour | Analyses/Day | Storage |
|------|---------------|--------------|---------|
| Free | 60 | 10 | 100MB |
| Pro | 600 | 1000 | 10GB |
| Enterprise | Unlimited | Unlimited | Unlimited |

**Response Headers:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705314600
```

---

## Pagination

All list endpoints support:
- `page`: Page number (1-indexed)
- `limit`: Items per page (1-100, default: 20)
- `sort_by`: Field to sort
- `sort_order`: asc or desc

---

## Summary

**Total Endpoints: 24**

| Category | Count |
|----------|-------|
| Authentication | 4 |
| Email Analysis | 5 |
| URL Analysis | 3 |
| Attachment Analysis | 1 |
| User Management | 4 |
| Threat Intelligence | 3 |
| Admin | 4 |

---

Next: Folder structure ve configuration setup.
