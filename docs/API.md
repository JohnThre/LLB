# LLB API Documentation

## Base URL
- Development: `http://localhost:8000/api/v1`
- Production: `https://api.llb.com/v1`

## Authentication
All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Core Endpoints

### Health Check
```http
GET /health
```
Returns system health status and version information.

### Authentication
```http
POST /auth/register
POST /auth/login
GET /auth/me
POST /auth/logout
```

### Chat Management
```http
GET /chats                    # List user chats
POST /chats                   # Create new chat
GET /chats/{id}/messages      # Get chat messages
POST /chats/{id}/messages     # Send message
WebSocket /ws/{chat_id}       # Real-time messaging
```

### AI Processing
```http
POST /ai/classify             # Text classification
POST /ai/extract-entities     # Entity extraction
POST /ai/generate             # Text generation
POST /ai/analyze-sentiment    # Sentiment analysis
```

### Voice Processing
```http
POST /voice/transcribe        # Audio to text
POST /voice/synthesize        # Text to speech
WebSocket /voice/stream       # Real-time audio
```

### Document Processing
```http
POST /documents/upload        # Upload document
POST /documents/analyze       # Analyze document
GET /documents/knowledge      # Search knowledge base
```

## Response Format
All API responses follow this structure:
```json
{
  "success": true,
  "data": {},
  "message": "Success",
  "timestamp": "2025-09-02T00:00:00Z"
}
```

## Error Handling
Error responses include:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  },
  "timestamp": "2025-09-02T00:00:00Z"
}
```

## Rate Limiting
- 100 requests per minute per user
- 1000 requests per hour per user
- WebSocket connections: 10 per user

## Interactive Documentation
Visit `/docs` for Swagger UI or `/redoc` for ReDoc interface.