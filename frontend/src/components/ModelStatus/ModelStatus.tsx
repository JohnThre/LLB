import React, { useEffect, useState } from "react";
import { 
  Box, 
  Paper, 
  Typography, 
  CircularProgress, 
  Chip, 
  LinearProgress,
  Avatar,
  Tooltip,
  IconButton,
} from "@mui/material";
import {
  Memory as MemoryIcon,
  Speed as SpeedIcon,
  Refresh as RefreshIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
} from "@mui/icons-material";
import { useTranslation } from "react-i18next";

interface ModelStatus {
  status: "loading" | "ready" | "error";
  modelName: string;
  lastUpdated?: string;
  memoryUsage?: number;
  responseTime?: number;
  version?: string;
}

export const ModelStatus: React.FC = () => {
  const { t } = useTranslation();
  const [modelStatus, setModelStatus] = useState<ModelStatus>({
    status: "loading",
    modelName: "Gemma 3 1B",
  });
  const [isRefreshing, setIsRefreshing] = useState(false);

  const fetchStatus = async () => {
    try {
      setIsRefreshing(true);
      const response = await fetch("/api/ai/model/status");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setModelStatus({
        ...data,
        lastUpdated: new Date().toISOString(),
      });
    } catch (error) {
      console.error("Error fetching model status:", error);
      setModelStatus((prev) => ({ 
        ...prev, 
        status: "error",
        lastUpdated: new Date().toISOString(),
      }));
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000); // Poll every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    switch (modelStatus.status) {
      case "ready":
        return "success";
      case "error":
        return "error";
      default:
        return "warning";
    }
  };

  const getStatusIcon = () => {
    switch (modelStatus.status) {
      case "ready":
        return <CheckCircleIcon sx={{ color: "success.main" }} />;
      case "error":
        return <ErrorIcon sx={{ color: "error.main" }} />;
      default:
        return <WarningIcon sx={{ color: "warning.main" }} />;
    }
  };

  const formatLastUpdated = () => {
    if (!modelStatus.lastUpdated) return "";
    const date = new Date(modelStatus.lastUpdated);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Paper
      elevation={2}
      sx={{
        p: 3,
        background: "linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.95) 100%)",
        backdropFilter: "blur(10px)",
        border: "1px solid rgba(0, 0, 0, 0.05)",
        borderRadius: 3,
        transition: "all 0.3s ease-in-out",
        "&:hover": {
          transform: "translateY(-2px)",
          boxShadow: "0px 8px 24px rgba(0, 0, 0, 0.12)",
        },
      }}
    >
      <Box sx={{ display: "flex", alignItems: "center", gap: 2, mb: 2 }}>
        <Avatar 
          sx={{ 
            bgcolor: getStatusColor() === "success" ? "success.main" : 
                   getStatusColor() === "error" ? "error.main" : "warning.main",
            width: 48,
            height: 48,
          }}
        >
          {modelStatus.status === "loading" ? (
            <CircularProgress size={24} color="inherit" />
          ) : (
            getStatusIcon()
          )}
        </Avatar>
        
        <Box sx={{ flex: 1 }}>
          <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 0.5 }}>
            <Typography variant="h6" sx={{ fontWeight: 600, color: "text.primary" }}>
              {t("modelStatus.title", "Model Status")}
            </Typography>
            <Chip
              label={t(`modelStatus.${modelStatus.status}`, modelStatus.status)}
              color={getStatusColor()}
              size="small"
              variant="outlined"
              sx={{ fontWeight: 600 }}
            />
          </Box>
          
          <Typography variant="body1" sx={{ color: "text.secondary", mb: 1 }}>
            {modelStatus.modelName}
            {modelStatus.version && (
              <Typography component="span" variant="caption" sx={{ ml: 1, opacity: 0.7 }}>
                v{modelStatus.version}
              </Typography>
            )}
          </Typography>
          
          {modelStatus.lastUpdated && (
            <Typography variant="caption" sx={{ color: "text.secondary" }}>
              {t("modelStatus.lastUpdated", "Last updated")}: {formatLastUpdated()}
            </Typography>
          )}
        </Box>

        <Tooltip title={t("modelStatus.refresh", "Refresh Status")}>
          <IconButton 
            onClick={fetchStatus} 
            disabled={isRefreshing}
            sx={{ 
              bgcolor: "rgba(25, 118, 210, 0.1)",
              "&:hover": { bgcolor: "rgba(25, 118, 210, 0.2)" },
            }}
          >
            <RefreshIcon 
              sx={{ 
                animation: isRefreshing ? "spin 1s linear infinite" : "none",
                "@keyframes spin": {
                  "0%": { transform: "rotate(0deg)" },
                  "100%": { transform: "rotate(360deg)" },
                },
              }} 
            />
          </IconButton>
        </Tooltip>
      </Box>

      {/* Performance Metrics */}
      {modelStatus.status === "ready" && (
        <Box sx={{ display: "flex", gap: 2, mt: 2 }}>
          {modelStatus.memoryUsage !== undefined && (
            <Box sx={{ flex: 1 }}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
                <MemoryIcon sx={{ fontSize: 16, color: "text.secondary" }} />
                <Typography variant="caption" sx={{ color: "text.secondary" }}>
                  {t("modelStatus.memoryUsage", "Memory")}
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={modelStatus.memoryUsage}
                sx={{
                  height: 6,
                  borderRadius: 3,
                  bgcolor: "rgba(0, 0, 0, 0.1)",
                  "& .MuiLinearProgress-bar": {
                    borderRadius: 3,
                    bgcolor: modelStatus.memoryUsage > 80 ? "error.main" : 
                            modelStatus.memoryUsage > 60 ? "warning.main" : "success.main",
                  },
                }}
              />
              <Typography variant="caption" sx={{ color: "text.secondary" }}>
                {modelStatus.memoryUsage}%
              </Typography>
            </Box>
          )}

          {modelStatus.responseTime !== undefined && (
            <Box sx={{ flex: 1 }}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
                <SpeedIcon sx={{ fontSize: 16, color: "text.secondary" }} />
                <Typography variant="caption" sx={{ color: "text.secondary" }}>
                  {t("modelStatus.responseTime", "Response Time")}
                </Typography>
              </Box>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                {modelStatus.responseTime}ms
              </Typography>
            </Box>
          )}
        </Box>
      )}

      {/* Loading Progress */}
      {modelStatus.status === "loading" && (
        <LinearProgress 
          sx={{ 
            mt: 2,
            height: 4,
            borderRadius: 2,
            bgcolor: "rgba(0, 0, 0, 0.1)",
            "& .MuiLinearProgress-bar": {
              borderRadius: 2,
              bgcolor: "primary.main",
            },
          }} 
        />
      )}
    </Paper>
  );
};
