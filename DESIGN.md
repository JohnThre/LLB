# LLB (爱学伴) - Local AI-Driven Sex Education Web Application

## Project Overview
LLB (爱学伴) is a web-based application designed to provide sex education through local AI processing. The application focuses on privacy, accessibility, and comprehensive educational content while maintaining local processing capabilities.

## System Requirements

### Minimum Hardware Requirements
- CPU: 8th Gen Intel Mobile i7
- RAM: 16GB
- Storage: 256GB SSD
- GPU: Integrated Graphics

### Recommended Hardware Requirements
- CPU: 9th Gen Intel Desktop i7 or better
- RAM: 32GB or more
- Storage: 512GB SSD or better
- GPU: NVIDIA RTX 3060 OC 12GB or better

### Software Requirements
- Ubuntu 22.04 LTS (WSL2)
- Windows 11 Pro
- Google Chrome (Primary browser)
- Node.js 18.x or later
- Python 3.10 or later
- Python virtual environment (llb-env)

## Technical Architecture

### Frontend
- Framework: React.js with TypeScript
- UI Components: Material-UI (MUI)
- State Management: Redux Toolkit
- Audio Processing: Web Audio API
- PDF Processing: PDF.js

### Backend
- Framework: FastAPI (Python)
- AI Model: Google's Gemma 3 1B
- Language Processing: 
  - Simplified Chinese (Mandarin)
  - Henan Dialect
  - American English
  - British English
- Document Processing: PyPDF2

### AI Components
- Text Processing: Gemma 3 1B
- Voice Processing: Whisper
- Language Detection: FastText
- Document Analysis: Custom PDF parser

### Data Storage
- Local SQLite database
- File system for document storage
- IndexedDB for browser-side caching

## Key Features

### 1. Multi-modal Input
- Text input
- Voice input
- PDF document upload
- Image upload (future)

### 2. Language Support
- Simplified Chinese (Mandarin)
- Henan Dialect
- American English
- British English

### 3. AI Processing
- Local text generation using Gemma 3 1B
- Voice-to-text conversion
- Document analysis
- Multi-language support

### 4. User Interface
- Responsive design
- Dark/Light mode
- Accessibility features
- Progressive Web App (PWA) support

### 5. Security & Privacy
- Local processing
- No data transmission
- End-to-end encryption
- Regular security audits

## Development Phases

### Phase 1: Foundation
- Project setup
- Basic UI implementation
- Local AI integration
- Database setup

### Phase 2: Core Features
- Text processing with Gemma 3 1B
- Voice processing
- PDF handling
- Multi-language support

### Phase 3: Optimization
- Performance tuning
- GPU acceleration
- Browser compatibility
- PWA implementation

### Phase 4: Testing & Deployment
- Unit testing
- Integration testing
- Performance testing
- Documentation

## Performance Optimization

### CPU Optimization
- Multi-threading for AI processing
- Efficient data structures
- Caching mechanisms

### GPU Optimization
- CUDA acceleration for Gemma 3 1B
- Batch processing
- Memory management

### Browser Optimization
- Code splitting
- Lazy loading
- Service workers
- IndexedDB caching

## Security Considerations
- Local data storage
- Input validation
- XSS prevention
- CSRF protection
- Regular security updates

## Future Enhancements
- Mobile app development
- Offline mode
- Additional language support
- Advanced AI features
- Community features

## Development Guidelines
- Clean code principles
- Maximum line length: 80 characters
- Maximum file length: 500 lines
- Comprehensive documentation
- Regular code reviews
- Automated testing 