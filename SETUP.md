# LLB (爱学伴) Setup Guide

## Development Environment Setup

### 1. System Requirements
- Ubuntu 22.04 LTS (WSL2)
- Windows 11 Pro
- NVIDIA RTX 3060 OC 12GB
- 32GB RAM
- 9th Gen Intel i7 CPU

### 2. WSL2 Setup
```bash
# Update WSL
wsl --update

# Set WSL2 as default
wsl --set-default-version 2

# Install Ubuntu 22.04
wsl --install -d Ubuntu-22.04
```

### 3. NVIDIA Driver Setup
```bash
# Install NVIDIA drivers
sudo apt update
sudo apt install nvidia-driver-525

# Install CUDA toolkit
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.3.1/local_installers/cuda-repo-ubuntu2204-12-3-local_12.3.1-545.23.08-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-3-local_12.3.1-545.23.08-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-3-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
```

### 4. Python Environment
```bash
# Activate existing virtual environment
source llb-env/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 5. Node.js Setup
```bash
# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install global dependencies
npm install -g yarn
```

## Project Structure
```
llb/
├── frontend/                 # React frontend
│   ├── public/              # Static files
│   ├── src/                 # Source code
│   │   ├── components/      # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── store/          # Redux store
│   │   └── utils/          # Utility functions
│   ├── package.json        # Frontend dependencies
│   └── tsconfig.json       # TypeScript config
│
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core functionality
│   │   ├── models/        # Data models
│   │   └── services/      # Business logic
│   ├── tests/             # Backend tests
│   └── requirements.txt    # Python dependencies
│
├── ai/                     # AI models and processing
│   ├── models/            # AI model files (Gemma 3 1B)
│   ├── processors/        # Data processors
│   └── utils/             # AI utilities
│
├── docs/                   # Documentation
├── llb-env/               # Python virtual environment
├── scripts/               # Build and utility scripts
├── .gitignore            # Git ignore file
├── README.md             # Project readme
└── docker-compose.yml    # Docker configuration
```

## Development Workflow

### 1. Clone Repository
```bash
git clone https://github.com/your-username/llb.git
cd llb
```

### 2. Install Dependencies
```bash
# Frontend
cd frontend
yarn install

# Backend
cd ../backend
source llb-env/bin/activate
pip install -r requirements.txt
```

### 3. Download AI Models
```bash
# Make sure you're in the virtual environment
source llb-env/bin/activate
python scripts/download_models.py
```

### 4. Start Development Servers
```bash
# Frontend (in frontend directory)
yarn dev

# Backend (in backend directory)
source llb-env/bin/activate
uvicorn app.main:app --reload
```

### 5. Running Tests
```bash
# Frontend tests
cd frontend
yarn test

# Backend tests
cd backend
source llb-env/bin/activate
pytest
```

## Git Workflow

### 1. Branch Naming Convention
- feature/feature-name
- bugfix/bug-description
- hotfix/issue-description
- release/version-number

### 2. Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

### 3. Pull Request Process
1. Create feature branch
2. Make changes
3. Write tests
4. Update documentation
5. Create pull request
6. Code review
7. Merge to main

## Deployment

### 1. Build Process
```bash
# Frontend build
cd frontend
yarn build

# Backend build
cd backend
source llb-env/bin/activate
python setup.py build
```

### 2. Local Deployment
```bash
# Using Docker
docker-compose up -d

# Manual deployment
./scripts/deploy.sh
```

## Monitoring and Maintenance

### 1. Logging
- Frontend: Browser console
- Backend: Application logs
- AI: Processing logs

### 2. Performance Monitoring
- CPU usage
- GPU utilization
- Memory consumption
- Response times

### 3. Regular Maintenance
- Dependency updates
- Security patches
- Performance optimization
- Database maintenance 