# Chat Functionality Documentation

## Overview

The chat functionality provides a comprehensive system for managing conversations between users and the AI assistant. It supports features like archiving, pinning, and message management.

## Features

- Create and manage chat sessions
- Send and receive messages
- Archive/unarchive chats
- Pin/unpin important chats
- Message history tracking
- Multi-language support
- Voice input support

## Database Schema

### Chat Table
- `id`: UUID (Primary Key)
- `title`: String
- `created_at`: DateTime
- `updated_at`: DateTime
- `is_archived`: Boolean
- `is_pinned`: Boolean
- `pinned_at`: DateTime (Nullable)

### Message Table
- `id`: UUID (Primary Key)
- `chat_id`: UUID (Foreign Key)
- `content`: String
- `role`: String (user/assistant)
- `created_at`: DateTime

## API Endpoints

### Chats

#### GET /api/chats
Get all chats with optional filters.
```json
{
  "archived": false,
  "pinned": true
}
```

#### POST /api/chats
Create a new chat.
```json
{
  "title": "New Chat"
}
```

#### GET /api/chats/{chat_id}
Get a specific chat by ID.

#### PUT /api/chats/{chat_id}
Update a chat.
```json
{
  "title": "Updated Title"
}
```

#### DELETE /api/chats/{chat_id}
Delete a chat.

#### POST /api/chats/{chat_id}/archive
Archive/unarchive a chat.
```json
{
  "archive": true
}
```

#### POST /api/chats/{chat_id}/pin
Pin/unpin a chat.
```json
{
  "pin": true
}
```

### Messages

#### GET /api/chats/{chat_id}/messages
Get all messages in a chat.

#### POST /api/chats/{chat_id}/messages
Send a new message.
```json
{
  "content": "Hello, AI!",
  "role": "user"
}
```

## Frontend Components

### Chat Component
The main chat interface component that handles:
- Message display
- Message input
- Voice input
- Real-time updates

### VoiceInput Component
A reusable component for voice recording and transcription:
- Microphone access
- Recording controls
- Processing status
- Multi-language support

## Usage Examples

### Creating a New Chat
```typescript
const response = await fetch('/api/chats', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'New Chat'
  })
});
```

### Sending a Message
```typescript
const response = await fetch(`/api/chats/${chatId}/messages`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    content: 'Hello, AI!',
    role: 'user'
  })
});
```

### Using Voice Input
```typescript
<VoiceInput
  onTranscriptionComplete={(text) => handleMessage(text)}
  language="en"
  disabled={isLoading}
/>
```

## Error Handling

The chat system includes comprehensive error handling:
- Invalid input validation
- Database operation errors
- API request failures
- Voice recording issues

## Security Considerations

- All endpoints require authentication
- Input sanitization
- Rate limiting
- Secure WebSocket connections

## Performance Optimization

- Pagination for message history
- Efficient database queries
- Caching strategies
- Optimized voice processing

## Testing

The chat functionality includes comprehensive tests:
- Unit tests for models and schemas
- Integration tests for API endpoints
- Frontend component tests
- Voice input tests

Run tests using:
```bash
pytest backend/tests/test_chat.py
``` 