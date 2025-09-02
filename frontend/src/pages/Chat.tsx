import React from "react";
import { Box, Container } from "@mui/material";
import { Chat as ChatComponent } from "../components/Chat/Chat";
import { ModelStatus } from "../components/ModelStatus/ModelStatus";
import { bauhausColors } from "../theme";

const Chat: React.FC = () => {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        backgroundColor: bauhausColors.gray[50],
        position: "relative",
        "&::before": {
          content: '""',
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "8px",
          background: `linear-gradient(90deg, ${bauhausColors.red} 0%, ${bauhausColors.red} 33%, ${bauhausColors.yellow} 33%, ${bauhausColors.yellow} 66%, ${bauhausColors.blue} 66%, ${bauhausColors.blue} 100%)`,
        },
      }}
    >
      <Container maxWidth="lg" sx={{ pt: 4, pb: 3, height: "calc(100vh - 48px)" }}>
        <Box 
          sx={{ 
            mb: 3,
            p: 2,
            backgroundColor: bauhausColors.white,
            border: `2px solid ${bauhausColors.black}`,
            boxShadow: `4px 4px 0px ${bauhausColors.gray[200]}`,
          }}
        >
          <ModelStatus />
        </Box>
        <Box 
          sx={{ 
            height: "calc(100vh - 200px)",
            backgroundColor: bauhausColors.white,
            border: `2px solid ${bauhausColors.black}`,
            boxShadow: `6px 6px 0px ${bauhausColors.gray[200]}`,
          }}
        >
          <ChatComponent />
        </Box>
      </Container>
    </Box>
  );
};

export default Chat;
