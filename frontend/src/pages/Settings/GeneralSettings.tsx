import React from "react";
import {
  Box,
  Typography,
  Switch,
  FormControlLabel,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  SelectChangeEvent,
} from "@mui/material";
import { useTranslation } from "react-i18next";

const GeneralSettings: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [settings, setSettings] = React.useState({
    language: i18n.language,
    darkMode: false,
    notifications: true,
    autoUpdate: true,
  });

  const handleSettingChange = (name: string, value: string | boolean) => {
    setSettings((prev) => ({ ...prev, [name]: value }));
  };

  const handleSwitchChange = (name: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    handleSettingChange(name, event.target.checked);
  };

  const handleSelectChange = (name: string) => (event: SelectChangeEvent) => {
    handleSettingChange(name, event.target.value);
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {t("settings.general")}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>{t("settings.language")}</InputLabel>
            <Select
              value={settings.language}
              onChange={handleSelectChange("language")}
              label={t("settings.language")}
            >
              <MenuItem value="en">English</MenuItem>
              <MenuItem value="es">Español</MenuItem>
              <MenuItem value="fr">Français</MenuItem>
              <MenuItem value="de">Deutsch</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        {[
          { key: "darkMode", labelKey: "settings.darkMode" },
          { key: "notifications", labelKey: "settings.notifications" },
          { key: "autoUpdate", labelKey: "settings.autoUpdate" },
        ].map(({ key, labelKey }) => (
          <Grid item xs={12} key={key}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings[key as keyof typeof settings] as boolean}
                  onChange={handleSwitchChange(key)}
                />
              }
              label={t(labelKey)}
            />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default GeneralSettings;
