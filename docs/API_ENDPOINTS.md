# 🔌 API Endpoints Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication Endpoints

### 1\. User Registration

```
POST /auth/register
```

**Request:**

```json
{
  "email": "user@example.com",
  "password": "secure\\\_password",
  "first\\\_name": "John",
  "last\\\_name": "Doe"
}
```

**Response (201 Created):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "first\\\_name": "John",
  "last\\\_name": "Doe",
  "created\\\_at": "2024-01-15T10:30:00Z"
}
```

**Error (400):**

```json
{
  "detail": "Email already exists"
}
```

---

### 2\. User Login

```
POST /auth/login
```

**Request:**

```json
{
  "email": "user@example.com",
  "password": "secure\\\_password"
}
```

**Response (200 OK):**

```json
{
  "access\\\_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh\\\_token": "eyJhbGciOiJIUzI1NiIs...",
  "token\\\_type": "bearer",
  "expires\\\_in": 3600
}
```

---

### 3\. Token Refresh

```
POST /auth/refresh
```

**Request Headers:**

```
Authorization: Bearer {refresh\\\_token}
```

**Response (200 OK):**

```json
{
  "access\\\_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires\\\_in": 3600
}
```

---

### 4\. Logout

```
POST /auth/logout
```

**Request Headers:**

```
Authorization: Bearer {access\\\_token}
```

**Response (200 OK):**

```json
{
  "message": "Successfully logged out"
}
```

---

## Email Analysis Endpoints

### 5\. Analyze Email

```
POST /analyze/email
```

**Request Headers:**

```
Authorization: Bearer {access\\\_token}
Content-Type: multipart/form-data
```

**Request Body (Form Data):**

```
email\\\_file: <.eml file or raw email text>
OR
raw\\\_email: "From: sender@example.com\\\\nTo: recipient@example.com\\\\n..."
```

**Response (202 Accepted):**

```json
{
  "id": 101,
  "status": "processing",
  "message": "Email is being analyzed",
  "estimated\\\_time\\\_ms": 500
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
    "received\\\_at": "2024-01-15T10:30:00Z"
  },
  "analysis": {
    "id": 101,
    "risk\\\_score": 0.87,
    "risk\\\_level": "HIGH",
    "confidence": 0.92,
    "explanation": {
      "summary": "This email shows strong indicators of phishing attack",
      "risk\\\_factors": \\\[
        "Domain not authenticated (SPF failed)",
        "Urgency keywords in subject line",
        "Links point to suspicious domain"
      ],
      "safe\\\_indicators": \\\[
        "No executable attachments"
      ]
    },
    "features": {
      "sender\\\_features": {...},
      "header\\\_features": {...},
      "subject\\\_features": {...},
      "body\\\_features": {...}
    },
    "suspicious\\\_links": \\\[
      {
        "url": "https://suspicious-bank.com/verify",
        "reputation": 0.15,
        "malicious": true
      }
    ],
    "created\\\_at": "2024-01-15T10:31:00Z",
    "processing\\\_time\\\_ms": 245
  }
}
```

---

### 6\. Get Analysis Result

```
GET /analyze/{id}
```

**Request Headers:**

```
Authorization: Bearer {access\\\_token}
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

### 7\. List Analysis History

```
GET /analyze/history?page=1\\\&limit=20\\\&risk\\\_level=HIGH\\\&sort\\\_by=created\\\_at
```

**Query Parameters:**

* `page`: Page number (default: 1)
* `limit`: Items per page (default: 20, max: 100)
* `risk\\\_level`: Filter by HIGH, MEDIUM, LOW
* `sort\\\_by`: created\_at, risk\_score (default: created\_at)
* `sort\\\_order`: asc, desc (default: desc)
* `from\\\_date`: ISO date filter
* `to\\\_date`: ISO date filter

**Response (200 OK):**

```json
{
  "total": 245,
  "page": 1,
  "limit": 20,
  "total\\\_pages": 13,
  "data": \\\[
    {
      "id": 105,
      "email": {
        "sender": "attacker@example.com",
        "subject": "Urgent: Update Payment",
        "received\\\_at": "2024-01-15T11:00:00Z"
      },
      "analysis": {
        "risk\\\_score": 0.95,
        "risk\\\_level": "HIGH",
        "confidence": 0.98,
        "created\\\_at": "2024-01-15T11:01:00Z"
      }
    }
    // ... more results
  ]
}
```

---

### 8\. Delete Analysis

```
DELETE /analyze/{id}
```

**Request Headers:**

```
Authorization: Bearer {access\\\_token}
```

**Response (204 No Content):**

```
(empty body)
```

---

### 9\. Batch Email Analysis

```
POST /analyze/batch/emails
```

**Request Headers:**

```
Authorization: Bearer {access\\\_token}
Content-Type: multipart/form-data
```

**Request Body:**

```
csv\\\_file: <file with emails>
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
  "batch\\\_id": "batch\\\_abc123",
  "total\\\_emails": 100,
  "status": "processing",
  "progress": {
    "processed": 0,
    "total": 100
  }
}
```

---

## URL Analysis Endpoints

### 10\. Analyze Single URL

```
POST /analyze/url
```

**Request Headers:**

```
Authorization: Bearer {access\\\_token}
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
    "reputation\\\_score": 0.15,
    "is\\\_malicious": true,
    "sources": {
      "virusTotal": {
        "malicious\\\_vendors": 45,
        "suspicious\\\_vendors": 12,
        "clean\\\_vendors": 3
      },
      "urlhaus": {
        "threat\\\_type": "phishing",
        "payload": "credential\\\_harvester"
      },
      "phishTank": {
        "verified": true,
        "phish\\\_id": "5123456"
      }
    }
  },
  "ssl": {
    "valid": false,
    "certificate\\\_data": {
      "issuer": "Unknown",
      "valid\\\_until": "2024-12-31"
    }
  },
  "analysis": {
    "structure\\\_analysis": {
      "has\\\_at\\\_symbol": false,
      "subdomain\\\_count": 1,
      "uses\\\_ip": false
    },
    "typosquatting\\\_score": 0.8,
    "last\\\_checked": "2024-01-15T10:30:00Z"
  },
  "created\\\_at": "2024-01-15T10:31:00Z"
}
```

---

### 11\. Batch URL Analysis

```
POST /analyze/urls/batch
```

**Request:**

```json
{
  "urls": \\\[
    "https://example.com",
    "https://suspicious.com",
    "https://malicious.net"
  ]
}
```

**Response (202 Accepted):**

```json
{
  "batch\\\_id": "batch\\\_url\\\_123",
  "urls": 3,
  "status": "processing"
}
```

**Get Batch Results:**

```
GET /analyze/batch/{batch\\\_id}
```

---

### 12\. URL History

```
GET /analyze/urls/history?limit=20
```

**Response:**

```json
{
  "total": 150,
  "data": \\\[
    {
      "id": 200,
      "url": "https://suspicious.com",
      "reputation\\\_score": 0.25,
      "is\\\_malicious": true,
      "last\\\_checked": "2024-01-15T10:30:00Z"
    }
    // ... more results
  ]
}
```

---

## Attachment Analysis Endpoints

### 13\. Analyze Attachment

```
POST /analyze/attachment
```

**Request Headers:**

```
Authorization: Bearer {access\\\_token}
Content-Type: multipart/form-data
```

**Request Body:**

```
file: <binary file>
email\\\_id: 50 (optional)
```

**Response (200 OK):**

```json
{
  "id": 300,
  "filename": "document.pdf",
  "file\\\_type": "pdf",
  "file\\\_size": 2048576,
  "analysis": {
    "is\\\_malicious": false,
    "confidence": 0.98,
    "risk\\\_factors": \\\[],
    "details": {
      "has\\\_macros": false,
      "is\\\_executable": false,
      "mime\\\_type\\\_correct": true,
      "scan\\\_results": {
        "virusTotal": {
          "malicious\\\_vendors": 0,
          "suspicious\\\_vendors": 0
        }
      }
    }
  },
  "created\\\_at": "2024-01-15T10:31:00Z"
}
```

---

## User Management Endpoints

### 14\. Get User Profile

```
GET /user/profile
```

**Request Headers:**

```
Authorization: Bearer {access\\\_token}
```

**Response (200 OK):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "first\\\_name": "John",
  "last\\\_name": "Doe",
  "role": "user",
  "is\\\_active": true,
  "stats": {
    "total\\\_analyses": 245,
    "high\\\_risk\\\_emails": 23,
    "avg\\\_processing\\\_time\\\_ms": 350
  },
  "created\\\_at": "2024-01-01T00:00:00Z",
  "updated\\\_at": "2024-01-15T10:00:00Z"
}
```

---

### 15\. Update User Profile

```
PUT /user/profile
```

**Request Body:**

```json
{
  "first\\\_name": "Jane",
  "last\\\_name": "Smith"
}
```

**Response (200 OK):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "first\\\_name": "Jane",
  "last\\\_name": "Smith",
  "updated\\\_at": "2024-01-15T12:00:00Z"
}
```

---

### 16\. Change Password

```
POST /user/change-password
```

**Request:**

```json
{
  "current\\\_password": "old\\\_password",
  "new\\\_password": "new\\\_secure\\\_password"
}
```

**Response (200 OK):**

```json
{
  "message": "Password changed successfully"
}
```

---

### 17\. Get User Statistics

```
GET /user/statistics
```

**Response (200 OK):**

```json
{
  "total\\\_analyses": 245,
  "analysis\\\_by\\\_risk": {
    "HIGH": 23,
    "MEDIUM": 65,
    "LOW": 157
  },
  "analysis\\\_by\\\_date": \\\[
    {
      "date": "2024-01-15",
      "count": 12
    },
    {
      "date": "2024-01-14",
      "count": 8
    }
  ],
  "top\\\_threats": \\\[
    {
      "threat\\\_type": "credential\\\_harvesting",
      "count": 45
    },
    {
      "threat\\\_type": "phishing",
      "count": 32
    }
  ],
  "avg\\\_response\\\_time\\\_ms": 350
}
```

---

## Threat Intelligence Endpoints

### 18\. Get Latest Threats

```
GET /threats/latest?limit=20
```

**Response (200 OK):**

```json
{
  "total": 1245,
  "data": \\\[
    {
      "id": 1,
      "threat\\\_type": "phishing\\\_campaign",
      "severity": "HIGH",
      "description": "Bank impersonation campaign targeting EU users",
      "indicators": {
        "domains": \\\["bank-verify.com", "bank-secure.net"],
        "keywords": \\\["verify account", "confirm identity"]
      },
      "first\\\_seen": "2024-01-10T00:00:00Z",
      "last\\\_seen": "2024-01-15T15:30:00Z",
      "count": 1234,
      "source": "community"
    }
    // ... more threats
  ]
}
```

---

### 19\. Get Threat Statistics

```
GET /threats/statistics?from\\\_date=2024-01-01\\\&to\\\_date=2024-01-15
```

**Response (200 OK):**

```json
{
  "total\\\_threats": 1245,
  "severity\\\_distribution": {
    "CRITICAL": 12,
    "HIGH": 234,
    "MEDIUM": 567,
    "LOW": 432
  },
  "threat\\\_types": {
    "phishing": 456,
    "malware": 234,
    "typosquatting": 123,
    "ceo\\\_fraud": 89
  },
  "trends": \\\[
    {
      "date": "2024-01-15",
      "new\\\_threats": 45,
      "active\\\_threats": 234
    }
  ],
  "geographic\\\_distribution": {
    "US": 345,
    "EU": 234,
    "ASIA": 123
  }
}
```

---

### 20\. Report New Threat

```
POST /threats/report
```

**Request:**

```json
{
  "threat\\\_type": "phishing\\\_campaign",
  "severity": "HIGH",
  "description": "Bank impersonation email campaign",
  "indicators": {
    "domains": \\\["suspicious-bank.com"],
    "sender\\\_patterns": \\\["noreply@\\\*suspicious\\\*"],
    "keywords": \\\["verify account"]
  }
}
```

**Response (201 Created):**

```json
{
  "id": 1246,
  "message": "Threat reported successfully",
  "verification\\\_status": "pending"
}
```

---

## Admin Endpoints

### 21\. Get All Users (Admin Only)

```
GET /admin/users?page=1\\\&limit=20
```

**Response:**

```json
{
  "total": 523,
  "data": \\\[
    {
      "id": 1,
      "email": "user@example.com",
      "role": "user",
      "is\\\_active": true,
      "created\\\_at": "2024-01-01T00:00:00Z",
      "stats": {
        "total\\\_analyses": 245,
        "high\\\_risk\\\_emails": 23
      }
    }
    // ... more users
  ]
}
```

---

### 22\. Get Platform Analytics (Admin Only)

```
GET /admin/analytics
```

**Response:**

```json
{
  "total\\\_users": 523,
  "active\\\_users": 412,
  "total\\\_analyses": 45234,
  "total\\\_high\\\_risk": 3245,
  "avg\\\_response\\\_time\\\_ms": 345,
  "model\\\_performance": {
    "accuracy": 0.96,
    "precision": 0.94,
    "recall": 0.93,
    "f1\\\_score": 0.935
  },
  "system\\\_health": {
    "database\\\_status": "healthy",
    "cache\\\_status": "healthy",
    "api\\\_uptime": 99.95
  }
}
```

---

### 23\. Retrain Model (Admin Only)

```
POST /admin/model/retrain
```

**Response (202 Accepted):**

```json
{
  "job\\\_id": "job\\\_abc123",
  "status": "queued",
  "estimated\\\_time\\\_seconds": 3600,
  "message": "Model retraining job has been queued"
}
```

**Get Retraining Status:**

```
GET /admin/model/retrain/{job\\\_id}
```

---

### 24\. Get System Logs (Admin Only)

```
GET /admin/logs?endpoint=/analyze/email\\\&status\\\_code=500\\\&limit=100
```

**Response:**

```json
{
  "total": 234,
  "data": \\\[
    {
      "id": 1,
      "timestamp": "2024-01-15T10:30:00Z",
      "user\\\_id": 1,
      "endpoint": "/analyze/email",
      "method": "POST",
      "status\\\_code": 500,
      "response\\\_time\\\_ms": 1234,
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
  "error\\\_code": "VALIDATION\\\_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `VALIDATION\\\_ERROR` | 400 | Input validation failed |
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | User doesn't have permission |
| `NOT\\\_FOUND` | 404 | Resource not found |
| `QUOTA\\\_EXCEEDED` | 429 | User quota exceeded |
| `INTERNAL\\\_ERROR` | 500 | Server error |

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

* `page`: Page number (1-indexed)
* `limit`: Items per page (1-100, default: 20)
* `sort\\\_by`: Field to sort
* `sort\\\_order`: asc or desc

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

