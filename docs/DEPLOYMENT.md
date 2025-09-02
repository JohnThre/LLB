# LLB Deployment Guide

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Development Setup
```bash
# Clone and setup
git clone <repository>
cd LLB

# Backend setup
cd backend
python3.11 -m venv llb-env
source llb-env/bin/activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Start development
make dev
```

## Production Deployment

### Docker Deployment (Recommended)
```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Manual Deployment
```bash
# Build frontend
cd frontend && npm run build

# Setup backend
cd ../backend
source llb-env/bin/activate
pip install -r requirements.txt

# Start services
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Environment Configuration

### Required Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/llb_db
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret

# AI Providers (Optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

## Health Monitoring

### Health Check Endpoints
- Backend: `http://localhost:8000/api/v1/health`
- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

### System Requirements
- **CPU**: 4+ cores recommended
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 50GB+ for models and data
- **GPU**: Optional, improves AI performance