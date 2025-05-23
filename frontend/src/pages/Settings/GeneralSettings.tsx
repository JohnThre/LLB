import React from 'react';
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
} from '@mui/material';
import { useTranslation } from 'react-i18next';

const GeneralSettings: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [settings, setSettings] = React.useState({
    language: i18n.language,
    darkMode: false,
    notifications: true,
    autoUpdate: true,
  });

  const handleChange = (name: string) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setSettings((prev) => ({
      ...prev,
      [name]: event.target.checked,
    }));
  };

  const handleSelectChange = (name: string) => (
    event: SelectChangeEvent
  ) => {
    setSettings((prev) => ({
      ...prev,
      [name]: event.target.value,
    }));
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {t('settings.general')}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>{t('settings.language')}</InputLabel>
            <Select
              value={settings.language}
              onChange={handleSelectChange('language')}
              label={t('settings.language')}
            >
              <MenuItem value="en">English</MenuItem>
              <MenuItem value="es">Español</MenuItem>
              <MenuItem value="fr">Français</MenuItem>
              <MenuItem value="de">Deutsch</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={settings.darkMode}
                onChange={handleChange('darkMode')}
              />
            }
            label={t('settings.darkMode')}
          />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={settings.notifications}
                onChange={handleChange('notifications')}
              />
            }
            label={t('settings.notifications')}
          />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={settings.autoUpdate}
                onChange={handleChange('autoUpdate')}
              />
            }
            label={t('settings.autoUpdate')}
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default GeneralSettings; 