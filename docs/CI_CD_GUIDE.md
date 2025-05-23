# CI/CD Guide for LLB Project

## 📋 Overview

The LLB project uses GitHub Actions for Continuous Integration (CI) and Continuous Deployment (CD) to ensure code quality, security, and reliable deployments.

## 🔄 Workflows

### 1. Continuous Integration (CI) - `.github/workflows/ci.yml`

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**

#### Backend Testing (`backend-test`)
- **Environment**: Ubuntu Latest with PostgreSQL 15 and Redis 7
- **Python Version**: 3.11
- **Steps**:
  1. Code checkout
  2. Python setup with dependency caching
  3. Install dependencies (including dev tools)
  4. Code linting with flake8
  5. Code formatting check with black
  6. Type checking with mypy
  7. Run tests with pytest and coverage
  8. Upload coverage to Codecov

#### Frontend Testing (`frontend-test`)
- **Environment**: Ubuntu Latest
- **Node.js Version**: 18
- **Steps**:
  1. Code checkout
  2. Node.js setup with npm caching
  3. Install dependencies
  4. ESLint linting
  5. TypeScript type checking
  6. Run tests with coverage
  7. Build application
  8. Upload coverage to Codecov

#### Security Scanning (`security-scan`)
- **Tools**:
  - Trivy vulnerability scanner
  - Bandit security linter (Python)
  - npm audit (Node.js)
- **Output**: SARIF reports uploaded to GitHub Security tab

#### Docker Build Testing (`docker-build`)
- **Dependencies**: Requires backend and frontend tests to pass
- **Actions**:
  - Build all Docker images (backend, frontend, nginx)
  - Use GitHub Actions cache for optimization
  - No push to registry (test only)

#### Integration Testing (`integration-test`)
- **Dependencies**: Requires Docker build to pass
- **Actions**:
  - Start services with docker-compose
  - Wait for services to be ready
  - Test health endpoints
  - Test API documentation
  - Clean up resources

#### Code Quality Analysis (`code-quality`)
- **Tool**: SonarCloud
- **Requirements**: `SONAR_TOKEN` secret

#### Dependency Checking (`dependency-check`)
- **Tools**:
  - Safety (Python dependencies)
  - npm audit (Node.js dependencies)

### 2. Continuous Deployment (CD) - `.github/workflows/cd.yml`

**Triggers:**
- Push to `main` branch (staging deployment)
- Push tags starting with `v*` (production deployment)
- Release published

**Jobs:**

#### Build and Push Images (`build-and-push`)
- **Registry**: GitHub Container Registry (ghcr.io)
- **Images Built**:
  - Backend: `ghcr.io/[owner]/[repo]-backend`
  - Frontend: `ghcr.io/[owner]/[repo]-frontend`
  - Nginx: `ghcr.io/[owner]/[repo]-nginx`
- **Platforms**: linux/amd64, linux/arm64
- **Tagging Strategy**:
  - Branch name for branch pushes
  - Semantic versioning for tags
  - SHA-based tags for commits

#### Staging Deployment (`deploy-staging`)
- **Trigger**: Push to `main` branch
- **Environment**: staging
- **Requirements**: Staging server secrets
- **Process**:
  1. Create deployment package
  2. SSH to staging server
  3. Pull latest images
  4. Rolling update deployment
  5. Run database migrations
  6. Health check verification

#### Production Deployment (`deploy-production`)
- **Trigger**: Version tags (`v*`)
- **Environment**: production
- **Requirements**: Production server secrets
- **Process**:
  1. Create production deployment package
  2. SSH to production server
  3. Create database backup
  4. Pull latest images
  5. Zero-downtime rolling update
  6. Run database migrations
  7. Health check verification

#### Security Scanning (`security-scan`)
- **Tool**: Trivy on built images
- **Output**: Vulnerability reports

#### Notifications (`notify`)
- **Tool**: Slack integration
- **Triggers**: Deployment success/failure

## 🔧 Setup Requirements

### GitHub Secrets

#### Required for CI:
```
GITHUB_TOKEN          # Automatically provided
SONAR_TOKEN          # SonarCloud integration
CODECOV_TOKEN        # Code coverage reporting
```

#### Required for CD:
```
# Staging Environment
STAGING_HOST         # Staging server hostname/IP
STAGING_USER         # SSH username for staging
STAGING_SSH_KEY      # Private SSH key for staging

# Production Environment
PRODUCTION_HOST      # Production server hostname/IP
PRODUCTION_USER      # SSH username for production
PRODUCTION_SSH_KEY   # Private SSH key for production

# Notifications
SLACK_WEBHOOK_URL    # Slack webhook for notifications
```

### Environment Variables

#### Staging Environment:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
SECRET_KEY=staging-secret-key
REACT_APP_API_URL=https://staging.example.com/api
```

#### Production Environment:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
SECRET_KEY=production-secret-key
REACT_APP_API_URL=https://llb.example.com/api
```

## 🚀 Deployment Process

### Staging Deployment

1. **Automatic Trigger**: Push to `main` branch
2. **Process**:
   ```bash
   # CI runs automatically
   git push origin main
   
   # Monitor deployment
   # Check GitHub Actions tab
   # Verify staging environment
   curl https://staging.example.com/api/v1/health
   ```

### Production Deployment

1. **Create Release Tag**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Monitor Deployment**:
   - Check GitHub Actions for deployment status
   - Verify production health checks
   - Monitor application metrics

### Manual Deployment

If needed, you can trigger manual deployments:

```bash
# Using GitHub CLI
gh workflow run cd.yml

# Or through GitHub web interface
# Go to Actions > Continuous Deployment > Run workflow
```

## 🧪 Testing Strategy

### Unit Tests
- **Backend**: pytest with coverage
- **Frontend**: Jest with React Testing Library
- **Coverage Target**: >80%

### Integration Tests
- **API Testing**: FastAPI test client
- **E2E Testing**: Docker Compose environment
- **Database Testing**: Test database with migrations

### Security Tests
- **Static Analysis**: Bandit, ESLint security rules
- **Dependency Scanning**: Safety, npm audit
- **Container Scanning**: Trivy
- **Code Quality**: SonarCloud

## 📊 Monitoring and Alerts

### GitHub Actions Monitoring
- **Workflow Status**: Check Actions tab
- **Failed Builds**: Automatic email notifications
- **Security Alerts**: GitHub Security tab

### Deployment Monitoring
- **Health Checks**: Automated endpoint testing
- **Slack Notifications**: Success/failure alerts
- **Log Monitoring**: Container logs via Docker

### Quality Gates
- **Code Coverage**: Minimum 80%
- **Security Vulnerabilities**: No high/critical issues
- **Code Quality**: SonarCloud quality gate
- **Test Success**: All tests must pass

## 🔍 Troubleshooting

### Common CI Issues

#### Test Failures
```bash
# Run tests locally
cd backend && pytest -v
cd frontend && npm test

# Check test coverage
cd backend && pytest --cov=.
cd frontend && npm test -- --coverage
```

#### Docker Build Issues
```bash
# Test Docker builds locally
docker build -t llb-backend ./backend
docker build -t llb-frontend ./frontend
docker build -t llb-nginx ./docker/nginx
```

#### Dependency Issues
```bash
# Update dependencies
cd backend && pip install -r requirements.txt
cd frontend && npm install

# Check for vulnerabilities
cd backend && safety check
cd frontend && npm audit
```

### Common CD Issues

#### Deployment Failures
1. **Check server connectivity**:
   ```bash
   ssh user@staging-server
   ssh user@production-server
   ```

2. **Verify environment variables**:
   ```bash
   # On deployment server
   docker-compose config
   ```

3. **Check service health**:
   ```bash
   # On deployment server
   docker-compose ps
   docker-compose logs
   ```

#### Image Pull Issues
```bash
# On deployment server
docker login ghcr.io
docker pull ghcr.io/[owner]/[repo]-backend:latest
```

## 📚 Best Practices

### Code Quality
- Write comprehensive tests
- Follow coding standards
- Use type hints (Python) and TypeScript
- Document complex functions
- Keep functions small and focused

### Security
- Never commit secrets
- Use environment variables
- Regularly update dependencies
- Follow security scanning recommendations
- Implement proper input validation

### Deployment
- Test in staging before production
- Use feature flags for risky changes
- Monitor deployment metrics
- Have rollback procedures ready
- Document deployment processes

### Performance
- Optimize Docker images
- Use multi-stage builds
- Implement caching strategies
- Monitor resource usage
- Profile application performance

## 🔄 Workflow Customization

### Adding New Jobs

1. **Edit workflow files**:
   ```yaml
   # .github/workflows/ci.yml
   new-job:
     runs-on: ubuntu-latest
     steps:
       - uses: actions/checkout@v4
       - name: Custom step
         run: echo "Custom job"
   ```

2. **Add dependencies**:
   ```yaml
   deploy:
     needs: [test, new-job]  # Add new-job as dependency
   ```

### Environment-Specific Configurations

1. **Create environment files**:
   ```bash
   # docker-compose.staging.yml
   # docker-compose.production.yml
   ```

2. **Update deployment scripts**:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
   ```

## 📖 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [SonarCloud Documentation](https://sonarcloud.io/documentation)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) 