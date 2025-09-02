import React from "react";
import {
  Box,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Typography,
  Divider,
  IconButton,
} from "@mui/material";
import { useTranslation } from "react-i18next";
import DeleteIcon from "@mui/icons-material/Delete";
import { format } from "date-fns";

interface ChatSession {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: Date;
}

const ChatHistory: React.FC = () => {
  const { t } = useTranslation();
  const [sessions, setSessions] = React.useState<ChatSession[]>([
    {
      id: "1",
      title: "General Discussion",
      lastMessage: "Hello, how can I help you?",
      timestamp: new Date(),
    },
  ]);

  const handleDelete = React.useCallback((id: string) => {
    setSessions((prev) => prev.filter((session) => session.id !== id));
  }, []);

  const renderChatSession = React.useCallback((session: ChatSession, index: number) => (
    <React.Fragment key={session.id}>
      <ListItem
        disablePadding
        secondaryAction={
          <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(session.id)}>
            <DeleteIcon />
          </IconButton>
        }
      >
        <ListItemButton>
          <ListItemText
            primary={session.title}
            secondary={
              <>
                <Typography component="span" variant="body2" color="text.primary">
                  {session.lastMessage}
                </Typography>
                {" — "}
                {format(session.timestamp, "MMM d, yyyy HH:mm")}
              </>
            }
          />
        </ListItemButton>
      </ListItem>
      {index < sessions.length - 1 && <Divider />}
    </React.Fragment>
  ), [handleDelete, sessions.length]);

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {t("chat.history")}
      </Typography>

      <List>
        {sessions.map(renderChatSession)}
      </List>
    </Box>
  );
};

export default ChatHistory;
