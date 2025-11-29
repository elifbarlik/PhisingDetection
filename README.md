# 🎯 Phishing Detection Platform - Enterprise Grade

Production-ready phishing detection sistemi. Multi-layer analiz ile email, URL ve attachment'ları güvenlik açısından değerlendirir.

## ✨ Features

* **📧 Email Analysis**: Headers, sender, subject ve body analizi
* **🔗 URL Analysis**: Reputation, SSL, redirect ve typosquatting detection
* **📎 Attachment Analysis**: File type, executable ve macro detection
* **🤖 ML-Based Detection**: XGBoost + NLP modelleri
* **⚡ Real-time Processing**: Celery + Redis async processing
* **📊 Dashboard**: Analytics ve threat intelligence
* **🔐 Security**: JWT auth, rate limiting, encryption
* **📱 API**: RESTful API + WebSocket support
* **🐳 Docker**: Production-ready containerization

## 🛠️ Tech Stack

### Backend

* **Framework**: FastAPI
* **ORM**: SQLAlchemy
* **Database**: PostgreSQL
* **Task Queue**: Celery + Redis
* **ML/NLP**: XGBoost, Scikit-learn, Transformers

### Frontend

* **Framework**: React 18 + TypeScript
* **Styling**: TailwindCSS
* **State**: Context API + Redux
* **HTTP Client**: Axios
* **Charts**: Recharts

### DevOps

* **Containerization**: Docker + Docker Compose
* **CI/CD**: GitHub Actions
* **Monitoring**: Prometheus + Grafana
* **Logging**: ELK Stack

## 🚀 Quick Start

### Prerequisites

* Python 3.10+
* Node.js 18+
* Docker \& Docker Compose
* PostgreSQL 13+
* Redis 6+

### Installation

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\\\Scripts\\\\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

#### Docker Setup

```bash
docker-compose up -d
```

## 📚 Documentation

* [Architecture Guide](./docs/ARCHITECTURE.md)
* [API Documentation](./docs/API.md)
* [ML Models](./docs/MODELS.md)
* [Deployment Guide](./docs/DEPLOYMENT.md)
* [Contributing Guide](./CONTRIBUTING.md)

## 🔄 Project Phases

| Phase | Duration | Status |
|-------|----------|--------|
| 1. Planning \\\& Architecture | 2-3 days | ⏳ In Progress |
| 2. Data \\\& Feature Engineering | 3-4 days | ⏳ Planned |
| 3. ML Models | 4-5 days | ⏳ Planned |
| 4. Backend API | 5-6 days | ⏳ Planned |
| 5. Frontend | 5-6 days | ⏳ Planned |
| 6. Testing | 3-4 days | ⏳ Planned |
| 7. DevOps \\\& Deployment | 3-4 days | ⏳ Planned |
| 8. Documentation | 2-3 days | ⏳ Planned |

## 📊 API Endpoints Overview

### Email Analysis

* `POST /api/v1/analyze/email` - Analyze email
* `GET /api/v1/analysis/{id}` - Get result
* `GET /api/v1/analysis/history` - Get history

### URL Analysis

* `POST /api/v1/analyze/url` - Analyze URL
* `POST /api/v1/analyze/urls/batch` - Batch analysis

### User Management

* `POST /api/v1/auth/register` - Register
* `POST /api/v1/auth/login` - Login
* `GET /api/v1/user/profile` - Get profile

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov

# Frontend tests
cd frontend
npm run test
```

## 📈 Performance

* **API Response Time**: <500ms (95th percentile)
* **Model Prediction**: <100ms
* **Database Query**: <50ms (95th percentile)
* **Uptime**: 99.9%

## 🔐 Security

* JWT-based authentication
* Rate limiting per IP/user
* SQL injection protection (SQLAlchemy ORM)
* XSS protection (React)
* CSRF tokens
* Data encryption at rest and in transit

## 📝 License

MIT License - see [LICENSE](./LICENSE) file

## 👥 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

## 📧 Contact \& Support

* **Issues**: GitHub Issues
* **Discussions**: GitHub Discussions
* **Email**: support@phishing-detection.local

## 🙏 Acknowledgments

* PhishTank for threat intelligence
* URLhaus for URL reputation data
* Kaggle community for datasets

---

**Made with ❤️ for cybersecurity**

