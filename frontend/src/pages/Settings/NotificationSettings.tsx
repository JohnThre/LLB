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

interface NotificationOption {
  key: string;
  labelKey: string;
}

interface NotificationSection {
  titleKey: string;
  options: NotificationOption[];
}

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

  const notificationSections: NotificationSection[] = [
    {
      titleKey: "settings.notificationChannels",
      options: [
        { key: "emailNotifications", labelKey: "settings.emailNotifications" },
        { key: "pushNotifications", labelKey: "settings.pushNotifications" },
        { key: "soundNotifications", labelKey: "settings.soundNotifications" },
      ],
    },
    {
      titleKey: "settings.notificationTypes",
      options: [
        { key: "messageNotifications", labelKey: "settings.messageNotifications" },
        { key: "mentionNotifications", labelKey: "settings.mentionNotifications" },
        { key: "updateNotifications", labelKey: "settings.updateNotifications" },
      ],
    },
    {
      titleKey: "settings.otherNotifications",
      options: [
        { key: "marketingNotifications", labelKey: "settings.marketingNotifications" },
      ],
    },
  ];

  const handleChange = (name: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    setSettings((prev) => ({ ...prev, [name]: event.target.checked }));
  };

  const renderNotificationSwitch = ({ key, labelKey }: NotificationOption) => (
    <FormControlLabel
      key={key}
      control={<Switch checked={settings[key as keyof typeof settings]} onChange={handleChange(key)} />}
      label={t(labelKey)}
    />
  );

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {t("settings.notifications")}
      </Typography>

      <Grid container spacing={3}>
        {notificationSections.map((section, index) => (
          <React.Fragment key={section.titleKey}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                {t(section.titleKey)}
              </Typography>
              <FormGroup>
                {section.options.map(renderNotificationSwitch)}
              </FormGroup>
            </Grid>
            {index < notificationSections.length - 1 && (
              <Grid item xs={12}>
                <Divider sx={{ my: 2 }} />
              </Grid>
            )}
          </React.Fragment>
        ))}
      </Grid>
    </Box>
  );
};

export default NotificationSettings;
