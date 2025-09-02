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
import { bauhausColors } from "../../theme";

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
        backgroundColor: bauhausColors.white,
        overflow: "hidden",
      }}
    >
      {/* Chat Header */}
      <Paper
        elevation={0}
        sx={{
          p: 3,
          backgroundColor: bauhausColors.blue,
          color: bauhausColors.white,
          borderRadius: 0,
          borderBottom: `4px solid ${bauhausColors.black}`,
        }}
      >
        <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
            <Box
              sx={{
                width: 48,
                height: 48,
                backgroundColor: bauhausColors.red,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                border: `2px solid ${bauhausColors.black}`,
              }}
            >
              <BotIcon sx={{ color: bauhausColors.white, fontSize: 28 }} />
            </Box>
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 700, color: bauhausColors.white }}>
                {t("app.name", "爱学伴 LLB")}
              </Typography>
              <Typography variant="body2" sx={{ color: bauhausColors.white, opacity: 0.8 }}>
                {t("chat.subtitle", "Your AI Sexual Health Education Assistant")}
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: "flex", gap: 1 }}>
            <Box
              sx={{
                px: 2,
                py: 1,
                backgroundColor: bauhausColors.yellow,
                color: bauhausColors.black,
                border: `2px solid ${bauhausColors.black}`,
                fontWeight: 700,
                fontSize: "0.75rem",
                textTransform: "uppercase",
                letterSpacing: "0.05em",
              }}
            >
              {t("chat.online", "Online")}
            </Box>
            <Tooltip title={t("chat.clearChat", "Clear Chat")}>
              <IconButton 
                onClick={clearChat} 
                sx={{
                  color: bauhausColors.white,
                  border: `2px solid ${bauhausColors.white}`,
                  borderRadius: 0,
                  "&:hover": {
                    backgroundColor: bauhausColors.red,
                  },
                }}
              >
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
          p: 3,
          backgroundColor: bauhausColors.gray[50],
          display: "flex",
          flexDirection: "column",
          gap: 2
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
              color: bauhausColors.gray[600],
            }}
          >
            <Box
              sx={{
                width: 80,
                height: 80,
                mb: 2,
                backgroundColor: bauhausColors.blue,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                border: `3px solid ${bauhausColors.black}`,
              }}
            >
              <BotIcon sx={{ fontSize: 40, color: bauhausColors.white }} />
            </Box>
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
                <Box
                  sx={{
                    width: 32,
                    height: 32,
                    backgroundColor: bauhausColors.blue,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    border: `2px solid ${bauhausColors.black}`,
                  }}
                >
                  <BotIcon sx={{ fontSize: 16, color: bauhausColors.white }} />
                </Box>
              )}
              
              <Box sx={{ maxWidth: "70%", minWidth: "200px" }}>
                <Paper
                  elevation={3}
                  sx={{
                    p: 2,
                    backgroundColor: message.role === "user" 
                      ? bauhausColors.red
                      : bauhausColors.white,
                    color: message.role === "user" 
                      ? bauhausColors.white
                      : bauhausColors.black,
                    borderRadius: 0,
                    border: `2px solid ${bauhausColors.black}`,
                    boxShadow: `3px 3px 0px ${bauhausColors.gray[200]}`,
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
                <Box
                  sx={{
                    width: 32,
                    height: 32,
                    backgroundColor: bauhausColors.yellow,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    border: `2px solid ${bauhausColors.black}`,
                  }}
                >
                  <PersonIcon sx={{ fontSize: 16, color: bauhausColors.black }} />
                </Box>
              )}
            </Box>
          </Grow>
        ))}

        {/* Typing Indicator */}
        {isTyping && (
          <Fade in={isTyping}>
            <Box sx={{ display: "flex", alignItems: "flex-end", gap: 1, mb: 2 }}>
              <Box
                sx={{
                  width: 32,
                  height: 32,
                  backgroundColor: bauhausColors.blue,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  border: `2px solid ${bauhausColors.black}`,
                }}
              >
                <BotIcon sx={{ fontSize: 16, color: bauhausColors.white }} />
              </Box>
              <Paper
                elevation={0}
                sx={{
                  p: 2,
                  backgroundColor: bauhausColors.white,
                  borderRadius: 0,
                  border: `2px solid ${bauhausColors.black}`,
                  boxShadow: `3px 3px 0px ${bauhausColors.gray[200]}`,
                }}
              >
                <Box sx={{ display: "flex", gap: 0.5, alignItems: "center" }}>
                  <Box
                    sx={{
                      width: 8,
                      height: 8,
                      borderRadius: "50%",
                      bgcolor: bauhausColors.blue,
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
                      bgcolor: bauhausColors.blue,
                      animation: "pulse 1.5s ease-in-out infinite 0.2s",
                    }}
                  />
                  <Box
                    sx={{
                      width: 8,
                      height: 8,
                      borderRadius: "50%",
                      bgcolor: bauhausColors.blue,
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
        <Box
          sx={{
            height: 4,
            backgroundColor: bauhausColors.gray[200],
            position: "relative",
            "&::after": {
              content: '""',
              position: "absolute",
              top: 0,
              left: 0,
              height: "100%",
              width: "30%",
              backgroundColor: bauhausColors.red,
              animation: "loading 1.5s ease-in-out infinite",
              "@keyframes loading": {
                "0%": { left: "-30%" },
                "100%": { left: "100%" },
              },
            },
          }}
        />
      )}

      {/* Input Area */}
      <Paper
        elevation={0}
        sx={{
          p: 2,
          backgroundColor: bauhausColors.white,
          borderRadius: 0,
          borderTop: `4px solid ${bauhausColors.yellow}`,
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
                backgroundColor: bauhausColors.gray[50],
                borderRadius: 0,
                "& fieldset": {
                  borderWidth: "2px",
                  borderColor: bauhausColors.gray[300],
                },
                "&:hover fieldset": {
                  borderColor: bauhausColors.gray[400],
                },
                "&.Mui-focused fieldset": {
                  borderColor: bauhausColors.blue,
                },
              },
            }}
          />
          
          <Tooltip title={t("chat.attachFile", "Attach File")}>
            <IconButton 
              disabled={isLoading}
              sx={{ 
                backgroundColor: bauhausColors.gray[100],
                color: bauhausColors.black,
                border: `2px solid ${bauhausColors.black}`,
                borderRadius: 0,
                "&:hover": { 
                  backgroundColor: bauhausColors.yellow,
                },
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
              borderRadius: 0,
              p: 0,
              backgroundColor: bauhausColors.red,
              color: bauhausColors.white,
              border: `2px solid ${bauhausColors.black}`,
              "&:hover": {
                backgroundColor: bauhausColors.black,
              },
              "&:disabled": {
                backgroundColor: bauhausColors.gray[300],
                color: bauhausColors.gray[500],
              },
            }}
          >
            {isLoading ? (
              <Box
                sx={{
                  width: 24,
                  height: 24,
                  border: `3px solid ${bauhausColors.white}`,
                  borderTop: `3px solid transparent`,
                  borderRadius: 0,
                  animation: "spin 1s linear infinite",
                  "@keyframes spin": {
                    "0%": { transform: "rotate(0deg)" },
                    "100%": { transform: "rotate(360deg)" },
                  },
                }}
              />
            ) : (
              <SendIcon />
            )}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};