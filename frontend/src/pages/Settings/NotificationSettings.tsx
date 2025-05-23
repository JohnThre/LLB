import React from "react";
import {
  Box,
  Typography,
  Switch,
  FormControlLabel,
  FormGroup,
  Divider,
  Grid,
} from "@mui/material";
import { useTranslation } from "react-i18next";

const NotificationSettings: React.FC = () => {
  const { t } = useTranslation();
  const [settings, setSettings] = React.useState({
    emailNotifications: true,
    pushNotifications: true,
    soundNotifications: true,
    messageNotifications: true,
    mentionNotifications: true,
    updateNotifications: true,
    marketingNotifications: false,
  });

  const handleChange =
    (name: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      setSettings((prev) => ({
        ...prev,
        [name]: event.target.checked,
      }));
    };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {t("settings.notifications")}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            {t("settings.notificationChannels")}
          </Typography>
          <FormGroup>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.emailNotifications}
                  onChange={handleChange("emailNotifications")}
                />
              }
              label={t("settings.emailNotifications")}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.pushNotifications}
                  onChange={handleChange("pushNotifications")}
                />
              }
              label={t("settings.pushNotifications")}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.soundNotifications}
                  onChange={handleChange("soundNotifications")}
                />
              }
              label={t("settings.soundNotifications")}
            />
          </FormGroup>
        </Grid>

        <Grid item xs={12}>
          <Divider sx={{ my: 2 }} />
        </Grid>

        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            {t("settings.notificationTypes")}
          </Typography>
          <FormGroup>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.messageNotifications}
                  onChange={handleChange("messageNotifications")}
                />
              }
              label={t("settings.messageNotifications")}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.mentionNotifications}
                  onChange={handleChange("mentionNotifications")}
                />
              }
              label={t("settings.mentionNotifications")}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.updateNotifications}
                  onChange={handleChange("updateNotifications")}
                />
              }
              label={t("settings.updateNotifications")}
            />
          </FormGroup>
        </Grid>

        <Grid item xs={12}>
          <Divider sx={{ my: 2 }} />
        </Grid>

        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            {t("settings.otherNotifications")}
          </Typography>
          <FormGroup>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.marketingNotifications}
                  onChange={handleChange("marketingNotifications")}
                />
              }
              label={t("settings.marketingNotifications")}
            />
          </FormGroup>
        </Grid>
      </Grid>
    </Box>
  );
};

export default NotificationSettings;
