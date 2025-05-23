import React from 'react';
import { Box, Container } from '@mui/material';
import { Chat as ChatComponent } from '../components/Chat/Chat';
import { ModelStatus } from '../components/ModelStatus/ModelStatus';

const Chat: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ height: '100vh', py: 2 }}>
      <Box sx={{ mb: 2 }}>
        <ModelStatus />
      </Box>
      <Box sx={{ height: 'calc(100vh - 120px)' }}>
        <ChatComponent />
      </Box>
    </Container>
  );
};

export default Chat; 