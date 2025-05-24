import React from "react";
import { Box, Container } from "@mui/material";
import { Chat as ChatComponent } from "../components/Chat/Chat";
import { ModelStatus } from "../components/ModelStatus/ModelStatus";

const Chat: React.FC = () => {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        py: 3,
      }}
    >
      <Container maxWidth="lg" sx={{ height: "calc(100vh - 48px)" }}>
        <Box sx={{ mb: 3 }}>
          <ModelStatus />
        </Box>
        <Box sx={{ height: "calc(100vh - 200px)" }}>
          <ChatComponent />
        </Box>
      </Container>
    </Box>
  );
};

export default Chat;
