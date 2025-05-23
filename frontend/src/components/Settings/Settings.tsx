import React, { useState, useEffect } from "react";
import {
  Box,
  Paper,
  Typography,
  Slider,
  Switch,
  FormControlLabel,
  Divider,
} from "@mui/material";
import { useTranslation } from "react-i18next";
import { Button } from "../common/Button";

interface ModelSettings {
  temperature: number;
  maxTokens: number;
  topP: number;
  topK: number;
  useQuantization: boolean;
}

export const Settings: React.FC = () => {
  const { t } = useTranslation();
  const [settings, setSettings] = useState<ModelSettings>({
    temperature: 0.7,
    maxTokens: 2048,
    topP: 0.95,
    topK: 40,
    useQuantization: true,
  });

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await fetch("/api/model/settings");
        const data = await response.json();
        setSettings(data);
      } catch (error) {
        console.error("Error fetching settings:", error);
      }
    };

    fetchSettings();
  }, []);

  const handleSave = async () => {
    try {
      await fetch("/api/model/settings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(settings),
      });
    } catch (error) {
      console.error("Error saving settings:", error);
    }
  };

  return (
    <Paper elevation={1} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        {t("settings.title")}
      </Typography>

      <Box sx={{ mb: 3 }}>
        <Typography gutterBottom>{t("settings.temperature")}</Typography>
        <Slider
          value={settings.temperature}
          onChange={(_, value) =>
            setSettings((prev) => ({
              ...prev,
              temperature: value as number,
            }))
          }
          min={0}
          max={1}
          step={0.1}
          valueLabelDisplay="auto"
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <Typography gutterBottom>{t("settings.maxTokens")}</Typography>
        <Slider
          value={settings.maxTokens}
          onChange={(_, value) =>
            setSettings((prev) => ({
              ...prev,
              maxTokens: value as number,
            }))
          }
          min={1}
          max={4096}
          step={1}
          valueLabelDisplay="auto"
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <Typography gutterBottom>{t("settings.topP")}</Typography>
        <Slider
          value={settings.topP}
          onChange={(_, value) =>
            setSettings((prev) => ({
              ...prev,
              topP: value as number,
            }))
          }
          min={0}
          max={1}
          step={0.05}
          valueLabelDisplay="auto"
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <Typography gutterBottom>{t("settings.topK")}</Typography>
        <Slider
          value={settings.topK}
          onChange={(_, value) =>
            setSettings((prev) => ({
              ...prev,
              topK: value as number,
            }))
          }
          min={1}
          max={100}
          step={1}
          valueLabelDisplay="auto"
        />
      </Box>

      <Divider sx={{ my: 2 }} />

      <FormControlLabel
        control={
          <Switch
            checked={settings.useQuantization}
            onChange={(e) =>
              setSettings((prev) => ({
                ...prev,
                useQuantization: e.target.checked,
              }))
            }
          />
        }
        label={t("settings.useQuantization")}
      />

      <Box sx={{ mt: 3, display: "flex", justifyContent: "flex-end" }}>
        <Button onClick={handleSave}>{t("settings.save")}</Button>
      </Box>
    </Paper>
  );
};
