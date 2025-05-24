import React, { useState, useRef, useEffect } from "react";
import {
  Box,
  Paper,
  TextField,
  Typography,
  CircularProgress,
  Avatar,
  Fade,
  Grow,
  IconButton,
  Tooltip,
  Chip,
  LinearProgress,
} from "@mui/material";
import {
  Send as SendIcon,
  Person as PersonIcon,
  SmartToy as BotIcon,
  AttachFile as AttachFileIcon,
  Clear as ClearIcon,
} from "@mui/icons-material";
import { Button } from "../common/Button";
import VoiceInput from "../common/VoiceInput";
import { useTranslation } from "react-i18next";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export const Chat: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (messageContent: string) => {
    if (!messageContent.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: messageContent.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await fetch("/api/v1/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          message: messageContent.trim(),
          language: i18n.language,
          cultural_context: "mainland_china"
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Simulate typing delay for better UX
      setTimeout(() => {
        const assistantMessage: Message = {
          role: "assistant",
          content: data.response,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
        setIsTyping(false);
      }, 1000);
    } catch (error) {
      console.error("Error sending message:", error);
      setTimeout(() => {
        const errorMessage: Message = {
          role: "assistant",
          content: t("chat.errorMessage", "Sorry, I encountered an error. Please try again."),
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
        setIsTyping(false);
      }, 1000);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceTranscription = (text: string) => {
    setInput(text);
    handleSend(text);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend(input);
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Box 
      sx={{ 
        height: "100%", 
        display: "flex", 
        flexDirection: "column",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        borderRadius: 3,
        overflow: "hidden",
      }}
    >
      {/* Chat Header */}
      <Paper
        elevation={0}
        sx={{
          p: 3,
          background: "rgba(255, 255, 255, 0.95)",
          backdropFilter: "blur(10px)",
          borderBottom: "1px solid rgba(0, 0, 0, 0.1)",
        }}
      >
        <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
            <Avatar sx={{ bgcolor: "primary.main" }}>
              <BotIcon />
            </Avatar>
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 600, color: "text.primary" }}>
                {t("app.name", "爱学伴 LLB")}
              </Typography>
              <Typography variant="body2" sx={{ color: "text.secondary" }}>
                {t("chat.subtitle", "Your AI Sexual Health Education Assistant")}
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: "flex", gap: 1 }}>
            <Chip 
              label={t("chat.online", "Online")} 
              color="success" 
              size="small" 
              variant="outlined"
            />
            <Tooltip title={t("chat.clearChat", "Clear Chat")}>
              <IconButton onClick={clearChat} size="small">
                <ClearIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      </Paper>

      {/* Messages Area */}
      <Box
        sx={{
          flex: 1,
          overflow: "auto",
          p: 2,
          background: "rgba(255, 255, 255, 0.1)",
          backdropFilter: "blur(10px)",
          display: "flex",
          flexDirection: "column",
          gap: 1
        }}
      >
        {messages.length === 0 && (
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              textAlign: "center",
              color: "white",
            }}
          >
            <Avatar sx={{ width: 80, height: 80, mb: 2, bgcolor: "rgba(255, 255, 255, 0.2)" }}>
              <BotIcon sx={{ fontSize: 40 }} />
            </Avatar>
            <Typography variant="h5" sx={{ mb: 1, fontWeight: 600 }}>
              {t("chat.welcome", "Welcome to LLB!")}
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.8, maxWidth: 400 }}>
              {t("chat.welcomeMessage", "I'm here to help you with sexual health education. Ask me anything!")}
            </Typography>
          </Box>
        )}

        {messages.map((message, index) => (
          <Grow key={index} in={true} timeout={500 + index * 100}>
            <Box
              sx={{
                display: "flex",
                justifyContent: message.role === "user" ? "flex-end" : "flex-start",
                mb: 2,
                alignItems: "flex-end",
                gap: 1,
              }}
            >
              {message.role === "assistant" && (
                <Avatar sx={{ bgcolor: "rgba(255, 255, 255, 0.2)", width: 32, height: 32 }}>
                  <BotIcon sx={{ fontSize: 18 }} />
                </Avatar>
              )}
              
              <Box sx={{ maxWidth: "70%", minWidth: "200px" }}>
                <Paper
                  elevation={3}
                  sx={{
                    p: 2,
                    bgcolor: message.role === "user" 
                      ? "primary.main" 
                      : "rgba(255, 255, 255, 0.95)",
                    color: message.role === "user" 
                      ? "primary.contrastText" 
                      : "text.primary",
                    borderRadius: message.role === "user" 
                      ? "20px 20px 4px 20px" 
                      : "20px 20px 20px 4px",
                    backdropFilter: "blur(10px)",
                    border: message.role === "assistant" 
                      ? "1px solid rgba(0, 0, 0, 0.1)" 
                      : "none",
                    width: "fit-content",
                    maxHeight: "none",
                    overflow: "visible"
                  }}
                >
                  <Typography 
                    sx={{ 
                      lineHeight: 1.6,
                      wordWrap: "break-word",
                      whiteSpace: "pre-wrap",
                      maxWidth: "100%",
                      overflow: "visible"
                    }}
                  >
                    {message.content}
                  </Typography>
                  <Typography 
                    variant="caption" 
                    sx={{ 
                      display: "block", 
                      mt: 1, 
                      opacity: 0.7,
                      textAlign: message.role === "user" ? "right" : "left"
                    }}
                  >
                    {formatTime(message.timestamp)}
                  </Typography>
                </Paper>
              </Box>

              {message.role === "user" && (
                <Avatar sx={{ bgcolor: "secondary.main", width: 32, height: 32 }}>
                  <PersonIcon sx={{ fontSize: 18 }} />
                </Avatar>
              )}
            </Box>
          </Grow>
        ))}

        {/* Typing Indicator */}
        {isTyping && (
          <Fade in={isTyping}>
            <Box sx={{ display: "flex", alignItems: "flex-end", gap: 1, mb: 2 }}>
              <Avatar sx={{ bgcolor: "rgba(255, 255, 255, 0.2)", width: 32, height: 32 }}>
                <BotIcon sx={{ fontSize: 18 }} />
              </Avatar>
              <Paper
                elevation={3}
                sx={{
                  p: 2,
                  bgcolor: "rgba(255, 255, 255, 0.95)",
                  borderRadius: "20px 20px 20px 4px",
                  backdropFilter: "blur(10px)",
                  border: "1px solid rgba(0, 0, 0, 0.1)",
                }}
              >
                <Box sx={{ display: "flex", gap: 0.5, alignItems: "center" }}>
                  <Box
                    sx={{
                      width: 8,
                      height: 8,
                      borderRadius: "50%",
                      bgcolor: "primary.main",
                      animation: "pulse 1.5s ease-in-out infinite",
                      "@keyframes pulse": {
                        "0%, 80%, 100%": { opacity: 0.3 },
                        "40%": { opacity: 1 },
                      },
                    }}
                  />
                  <Box
                    sx={{
                      width: 8,
                      height: 8,
                      borderRadius: "50%",
                      bgcolor: "primary.main",
                      animation: "pulse 1.5s ease-in-out infinite 0.2s",
                    }}
                  />
                  <Box
                    sx={{
                      width: 8,
                      height: 8,
                      borderRadius: "50%",
                      bgcolor: "primary.main",
                      animation: "pulse 1.5s ease-in-out infinite 0.4s",
                    }}
                  />
                </Box>
              </Paper>
            </Box>
          </Fade>
        )}

        <div ref={messagesEndRef} />
      </Box>

      {/* Loading Progress */}
      {isLoading && (
        <LinearProgress 
          sx={{ 
            height: 2,
            bgcolor: "rgba(255, 255, 255, 0.2)",
            "& .MuiLinearProgress-bar": {
              bgcolor: "secondary.main",
            },
          }} 
        />
      )}

      {/* Input Area */}
      <Paper
        elevation={0}
        sx={{
          p: 2,
          background: "rgba(255, 255, 255, 0.95)",
          backdropFilter: "blur(10px)",
          borderTop: "1px solid rgba(0, 0, 0, 0.1)",
        }}
      >
        <Box sx={{ display: "flex", gap: 1, alignItems: "flex-end" }}>
          <VoiceInput
            onTranscriptionComplete={handleVoiceTranscription}
            language={i18n.language}
            disabled={isLoading}
          />
          
          <TextField
            ref={inputRef}
            fullWidth
            multiline
            maxRows={4}
            variant="outlined"
            placeholder={t("chat.inputPlaceholder", "Type your message here...")}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            sx={{
              "& .MuiOutlinedInput-root": {
                bgcolor: "background.paper",
                "& fieldset": {
                  borderColor: "rgba(0, 0, 0, 0.1)",
                },
              },
            }}
          />
          
          <Tooltip title={t("chat.attachFile", "Attach File")}>
            <IconButton 
              color="primary" 
              disabled={isLoading}
              sx={{ 
                bgcolor: "rgba(25, 118, 210, 0.1)",
                "&:hover": { bgcolor: "rgba(25, 118, 210, 0.2)" },
              }}
            >
              <AttachFileIcon />
            </IconButton>
          </Tooltip>
          
          <Button
            variant="contained"
            onClick={() => handleSend(input)}
            disabled={isLoading || !input.trim()}
            sx={{
              minWidth: 56,
              height: 56,
              borderRadius: "50%",
              p: 0,
              background: "linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)",
              "&:hover": {
                background: "linear-gradient(45deg, #1565c0 30%, #1976d2 90%)",
              },
            }}
          >
            {isLoading ? (
              <CircularProgress size={24} color="inherit" />
            ) : (
              <SendIcon />
            )}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};
