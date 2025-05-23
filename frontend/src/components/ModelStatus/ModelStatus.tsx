import React, { useEffect, useState } from "react";
import { Box, Paper, Typography, CircularProgress, Chip } from "@mui/material";
import { useTranslation } from "react-i18next";

interface ModelStatus {
  status: "loading" | "ready" | "error";
  modelName: string;
  lastUpdated?: string;
}

export const ModelStatus: React.FC = () => {
  const { t } = useTranslation();
  const [modelStatus, setModelStatus] = useState<ModelStatus>({
    status: "loading",
    modelName: "Gemma 3 1B",
  });

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch("/api/model/status");
        const data = await response.json();
        setModelStatus(data);
      } catch (error) {
        console.error("Error fetching model status:", error);
        setModelStatus((prev) => ({ ...prev, status: "error" }));
      }
    };

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

  return (
    <Paper
      elevation={1}
      sx={{
        p: 2,
        display: "flex",
        alignItems: "center",
        gap: 2,
      }}
    >
      {modelStatus.status === "loading" && <CircularProgress size={24} />}
      <Box sx={{ flex: 1 }}>
        <Typography variant="subtitle1" gutterBottom>
          {t("modelStatus.title")}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {modelStatus.modelName}
        </Typography>
      </Box>
      <Chip
        label={t(`modelStatus.${modelStatus.status}`)}
        color={getStatusColor()}
        size="small"
      />
    </Paper>
  );
};
