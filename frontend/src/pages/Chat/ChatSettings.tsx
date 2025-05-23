import React from "react";
import {
  Box,
  Typography,
  Switch,
  FormControlLabel,
  Slider,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  SelectChangeEvent,
} from "@mui/material";
import { useTranslation } from "react-i18next";

const ChatSettings: React.FC = () => {
  const { t } = useTranslation();
  const [settings, setSettings] = React.useState({
    autoSave: true,
    messageHistory: 100,
    theme: "light",
    fontSize: 16,
    soundEnabled: true,
  });

  const handleChange =
    (name: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      setSettings((prev) => ({
        ...prev,
        [name]: event.target.checked,
      }));
    };

  const handleSliderChange =
    (name: string) => (_: Event, value: number | number[]) => {
      setSettings((prev) => ({
        ...prev,
        [name]: value,
      }));
    };

  const handleSelectChange = (name: string) => (event: SelectChangeEvent) => {
    setSettings((prev) => ({
      ...prev,
      [name]: event.target.value,
    }));
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {t("chat.settings")}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={settings.autoSave}
                onChange={handleChange("autoSave")}
              />
            }
            label={t("chat.autoSave")}
          />
        </Grid>

        <Grid item xs={12}>
          <Typography gutterBottom>{t("chat.messageHistory")}</Typography>
          <Slider
            value={settings.messageHistory}
            onChange={handleSliderChange("messageHistory")}
            min={10}
            max={1000}
            step={10}
            marks
            valueLabelDisplay="auto"
          />
        </Grid>

        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>{t("chat.theme")}</InputLabel>
            <Select
              value={settings.theme}
              onChange={handleSelectChange("theme")}
              label={t("chat.theme")}
            >
              <MenuItem value="light">{t("chat.lightTheme")}</MenuItem>
              <MenuItem value="dark">{t("chat.darkTheme")}</MenuItem>
              <MenuItem value="system">{t("chat.systemTheme")}</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <Typography gutterBottom>{t("chat.fontSize")}</Typography>
          <Slider
            value={settings.fontSize}
            onChange={handleSliderChange("fontSize")}
            min={12}
            max={24}
            step={1}
            marks
            valueLabelDisplay="auto"
          />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={settings.soundEnabled}
                onChange={handleChange("soundEnabled")}
              />
            }
            label={t("chat.soundEnabled")}
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default ChatSettings;
