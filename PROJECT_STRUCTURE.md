# LLB Project Structure

## Overview
This document outlines the improved project structure for the LLB (爱学伴) sexual health education web application.

## Root Directory Structure
```
LLB/
├── .github/                    # GitHub workflows and templates
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── cd.yml
│   │   └── security.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── .vscode/                    # VS Code configuration
│   ├── settings.json
│   ├── launch.json
│   └── extensions.json
├── backend/                    # FastAPI backend application
│   ├── app/                    # Main application code
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Configuration management
│   │   ├── dependencies.py    # Dependency injection
│   │   ├── api/               # API routes
│   │   │   ├── __init__.py
│   │   │   ├── v1/            # API version 1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chat.py
│   │   │   │   ├── voice.py
│   │   │   │   ├── documents.py
│   │   │   │   └── health.py
│   │   │   └── deps.py        # API dependencies
│   │   ├── core/              # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── exceptions.py
│   │   ├── models/            # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   ├── voice.py
│   │   │   └── documents.py
│   │   ├── services/          # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py
│   │   │   ├── audio_service.py
│   │   │   ├── document_service.py
│   │   │   └── language_service.py
│   │   └── utils/             # Utility functions
│   │       ├── __init__.py
│   │       ├── validators.py
│   │       └── helpers.py
│   ├── tests/                 # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── alembic/               # Database migrations
│   ├── static/                # Static files
│   ├── uploads/               # File uploads
│   ├── logs/                  # Application logs
│   ├── requirements/          # Requirements files
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   └── prod.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── pyproject.toml
├── frontend/                  # React frontend application
│   ├── public/                # Public assets
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── icons/
│   ├── src/                   # Source code
│   │   ├── components/        # Reusable components
│   │   │   ├── common/        # Common UI components
│   │   │   ├── chat/          # Chat-related components
│   │   │   ├── voice/         # Voice-related components
│   │   │   └── documents/     # Document-related components
│   │   ├── pages/             # Page components
│   │   │   ├── Home/
│   │   │   ├── Chat/
│   │   │   └── Settings/
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API services
│   │   ├── store/             # Redux store
│   │   │   ├── slices/
│   │   │   └── middleware/
│   │   ├── utils/             # Utility functions
│   │   ├── types/             # TypeScript type definitions
│   │   ├── constants/         # Application constants
│   │   ├── locales/           # Internationalization
│   │   ├── styles/            # Global styles
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── config.ts
│   ├── tests/                 # Frontend tests
│   │   ├── __tests__/
│   │   ├── __mocks__/
│   │   └── utils/
│   ├── .env.example
│   ├── .eslintrc.js
│   ├── .prettierrc
│   ├── tsconfig.json
│   ├── package.json
│   └── webpack.config.js
├── ai/                        # AI models and processing
│   ├── models/                # Model files and configs
│   │   ├── gemma/
│   │   ├── whisper/
│   │   └── configs/
│   ├── processors/            # Data processors
│   │   ├── __init__.py
│   │   ├── text_processor.py
│   │   ├── audio_processor.py
│   │   └── document_processor.py
│   ├── prompts/               # Prompt templates
│   │   ├── __init__.py
│   │   ├── base_prompts.py
│   │   ├── safety_prompts.py
│   │   └── cultural_prompts.py
│   ├── utils/                 # AI utilities
│   │   ├── __init__.py
│   │   ├── model_loader.py
│   │   └── tokenizer.py
│   ├── cache/                 # Model cache
│   ├── temp/                  # Temporary files
│   ├── config.py
│   ├── prompt_engine.py
│   └── factory.py
├── docs/                      # Documentation
│   ├── api/                   # API documentation
│   ├── deployment/            # Deployment guides
│   ├── development/           # Development guides
│   ├── user/                  # User documentation
│   └── architecture/          # Architecture documentation
├── scripts/                   # Build and utility scripts
│   ├── setup/                 # Setup scripts
│   │   ├── install_deps.sh
│   │   ├── setup_env.sh
│   │   └── download_models.sh
│   ├── build/                 # Build scripts
│   │   ├── build_frontend.sh
│   │   ├── build_backend.sh
│   │   └── build_all.sh
│   ├── deploy/                # Deployment scripts
│   │   ├── deploy_local.sh
│   │   └── deploy_prod.sh
│   └── utils/                 # Utility scripts
│       ├── clean.sh
│       └── backup.sh
├── config/                    # Configuration files
│   ├── development.yml
│   ├── production.yml
│   └── testing.yml
├── docker/                    # Docker configurations
│   ├── backend/
│   ├── frontend/
│   └── nginx/
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── .dockerignore              # Docker ignore rules
├── docker-compose.yml         # Docker compose configuration
├── docker-compose.dev.yml     # Development docker compose
├── Makefile                   # Build automation
├── README.md                  # Project overview
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # License file
├── CHANGELOG.md               # Change log
└── pyproject.toml             # Python project configuration

## Key Improvements

### 1. Modular Architecture
- Clear separation of concerns
- Organized by feature and layer
- Reusable components

### 2. Configuration Management
- Environment-specific configurations
- Centralized configuration files
- Secure secret management

### 3. Testing Structure
- Unit, integration, and E2E tests
- Separate test configurations
- Mock and fixture organization

### 4. Build System
- Automated build scripts
- Docker containerization
- CI/CD pipeline support

### 5. Documentation
- Comprehensive documentation structure
- API documentation
- Development guides

### 6. Code Quality
- Linting and formatting configurations
- Pre-commit hooks
- Code quality standards

## File Naming Conventions

### Python Files
- snake_case for modules and functions
- PascalCase for classes
- UPPER_CASE for constants

### TypeScript/JavaScript Files
- camelCase for variables and functions
- PascalCase for components and classes
- kebab-case for file names

### Configuration Files
- lowercase with extensions
- Environment-specific suffixes

## Directory Guidelines

### Backend (`backend/`)
- Follow FastAPI best practices
- Separate API routes by version
- Use dependency injection
- Implement proper error handling

### Frontend (`frontend/`)
- Follow React best practices
- Component-based architecture
- State management with Redux
- TypeScript for type safety

### AI (`ai/`)
- Modular AI processing
- Efficient model loading
- Caching mechanisms
- Performance optimization

### Documentation (`docs/`)
- Markdown format
- Clear structure
- Code examples
- Regular updates

This structure provides a solid foundation for the LLB project, ensuring maintainability, scalability, and ease of development. 